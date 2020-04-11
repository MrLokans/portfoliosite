import datetime
from collections import defaultdict

import itertools
import json
import logging
import os
from typing import Dict, List, Set, Tuple, Iterable

import pandas as pd

from rest_framework.exceptions import ValidationError
from tqdm import tqdm

from apps.apartments_analyzer.enums import BulletinType
from apps.apartments_analyzer.services.subway_distance_calculator import (
    ApartmentDistanceEnricher,
)
from .api.serializers import RentApartmentSerializer, SoldApartmentSerializer
from .models import RentApartment, ApartmentScrapingResults, SoldApartments, PrecalculatedApartmentStats

RENTED_SUFFIX, SOLD_SUFFIX = "/ak/", "/pk/"


def q25(x):
    return x.quantile(0.25)


def q50(x):
    return x.quantile(0.5)


def q90(x):
    return x.quantile(0.9)


def q99(x):
    return x.quantile(0.99)


class StatisticsAggregator:

    SOLD_AGGREGATES = {
        'price_USD': ['mean', q25, q50, q90, q99],
        'total_area': ['mean', q25, q50, q90, q99],
        'living_area': ['mean', q25, q50, q90, q99],
    }
    RENT_AGGREGATES = {
        'price_USD': ['mean', q25, q50, q90, q99],
    }

    def __init__(self, filename):
        self.dataframe = pd.read_json(filename)
        self.prepare_dataframe()

    def prepare_dataframe(self):
        for money_field in ('price_USD', 'price_BYN'):
            self.dataframe[money_field] = self.dataframe[money_field].str.replace(" ", "")
            self.dataframe[money_field] = self.dataframe[money_field].astype(float)

    def reshaped_aggregates(self, aggregates):
        # {('price_USD', 'mean'): {1: 64771.463558765594, 2: 85659.79591836735}}
        # -> {1: {'price_USD': {'mean': 64771.463558765594}}}
        as_dict = aggregates.to_dict()
        new_aggregate = defaultdict(
            lambda: defaultdict(lambda: {})
        )
        for (second_level, third_level), room_values in as_dict.items():
            for root_key, final_value in room_values.items():
                new_aggregate[root_key][second_level][third_level] = final_value
        return new_aggregate

    def calculate_aggregates(self) -> dict:
        rent = self.dataframe[self.dataframe.origin_url.str.contains('/ak/')]
        sold = self.dataframe[self.dataframe.origin_url.str.contains('/pk/')]
        rent_stats = rent.groupby('room_count').agg(self.RENT_AGGREGATES)
        sold_stats = sold.groupby('room_count').agg(self.SOLD_AGGREGATES)
        return {
            'sold': self.reshaped_aggregates(sold_stats),
            'rent': self.reshaped_aggregates(rent_stats),
        }


class ApartmentDataImporter:
    """
    Take care of importing apartment data into
    the database
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._run_stats = self.get_initial_stats()
        self._progress_notifier = None
        self._reset_urls()

    def save_apartments_data(
        self, new_apartments, apartments_to_update, inactive_urls: Set[str]
    ):
        try:
            self._handle_database_sync(
                new_apartments, apartments_to_update, inactive_urls
            )
        except Exception as exc:
            self.logger.exception("Error saving changes to the database.")
            self._run_stats["succeeded"] = False
            self._run_stats["error_message"] = str(exc)
        finally:
            self._run_stats["time_finished"] = datetime.datetime.utcnow()
            if self.invalid_urls:
                self._run_stats["succeeded"] = False
            self._run_stats["invalid_urls"] = self.invalid_urls
            stats = ApartmentScrapingResults(**self._run_stats)
            stats.save()
            self.report_run_statistics()
            self.reset()

    def load_from_json(self, filename: str):
        """
        Reads parsed JSON file and attempts
        to create database entries from it
        """
        self.logger.info("Loading apartments data from file (%s)", filename)
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Filename {filename} does not exist.")
        with open(filename) as fd:
            json_items = json.load(fd)
        self.load_from_serialized_values(json_items)
        self.save_stat_aggregates(filename)

    def load_from_serialized_values(self, items: List[Dict]):
        existing_urls = self._get_existing_apartment_urls()
        loaded_urls = set(i["origin_url"] for i in items)
        inactive_urls = existing_urls - loaded_urls
        new_urls = loaded_urls - existing_urls
        updated_urls = loaded_urls - new_urls
        new_apartments = (i for i in items if i["origin_url"] in new_urls)
        apartments_to_update = (i for i in items if i["origin_url"] in updated_urls)
        self._progress_notifier = tqdm(total=len(new_urls) + len(updated_urls))
        self.save_apartments_data(new_apartments, apartments_to_update, inactive_urls)

    def save_stat_aggregates(self, filename):
        aggregates = StatisticsAggregator(filename).calculate_aggregates()
        PrecalculatedApartmentStats.objects.create(statistics=aggregates)

    def report_run_statistics(self):
        self.logger.info(self._run_stats)

    def get_initial_stats(self) -> dict:
        return {
            "total_errors": 0,
            "total_active": 0,
            "total_inactive": 0,
            "total_saved": 0,
            "new_items": 0,
            "updated_items": 0,
            "error_message": "",
            "succeeded": True,
            "time_started": datetime.datetime.utcnow(),
            "time_finished": None,
            "invalid_urls": [],
        }

    def model_for_url(self, url: str):
        if RENTED_SUFFIX in url:
            return RentApartment
        if SOLD_SUFFIX in url:
            return SoldApartments
        raise ValueError("No model can support this url type: {}".format(url))

    def reset(self):
        self._reset_urls()
        self._run_stats = self.get_initial_stats()
        if self._progress_notifier is not None:
            self._progress_notifier.close()
            self._progress_notifier = None

    def _reset_urls(self):
        self.inactive_urls = []
        self.active_urls = []
        self.invalid_urls = []

    def _get_existing_apartment_urls(self) -> Set[str]:
        """
        Gets list of apartment URLs already
        persisted to the database.
        """
        existing_apartments = itertools.chain(
            RentApartment.objects.urls(), SoldApartments.objects.urls()
        )
        return set(existing_apartments)

    def _get_serializer_for_scrapy_item(self, scrapy_item: dict):
        bulletin_type = scrapy_item["bulletin_type"]
        if bulletin_type == BulletinType.FOR_RENT.value:
            return RentApartmentSerializer
        if bulletin_type == BulletinType.FOR_SELL.value:
            return SoldApartmentSerializer
        raise ValueError("Unknown scrapy item type: {}".format(bulletin_type))

    def _attempt_saving_item(
        self, item_data: Dict, update: bool = False, instance=None
    ):
        serializer_args = {}
        processed_url = item_data["origin_url"]
        if update:
            serializer_args.update({"instance": instance})
        ser = self._get_serializer_for_scrapy_item(item_data)
        try:
            ser.validate_and_save(input_data=item_data, **serializer_args)
            self._run_stats["total_saved"] += 1
            if update:
                self._run_stats["updated_items"] += 1
            else:
                self._run_stats["new_items"] += 1
            self.active_urls.append(processed_url)
        except ValidationError as exc:
            self.logger.error("Invalid payload: %s", exc)
            self._run_stats["total_errors"] += 1
            self.invalid_urls.append(processed_url)
        except Exception:
            self.logger.exception("Error saving data %s.", ser.validated_data)
            self._run_stats["total_errors"] += 1
            self.invalid_urls.append(processed_url)
        finally:
            self._progress_notifier.update()

    def get_urls_by_type(self, urls: Iterable[str]) -> Tuple[List[str], List[str]]:
        rented_urls, sold_urls = [], []
        for url in urls:
            if RENTED_SUFFIX in url:
                rented_urls.append(url)
            elif SOLD_SUFFIX in url:
                sold_urls.append(url)
            else:
                raise ValueError(f"Unknown url type: {url}")
        return rented_urls, sold_urls

    def _handle_database_sync(
        self, new_apartments, apartments_to_update, inactive_urls: Set[str]
    ):
        inactive_rented_urls, inactive_sold_urls = self.get_urls_by_type(inactive_urls)
        self._run_stats["total_inactive"] = RentApartment.objects.mark_inactive(
            inactive_rented_urls
        ) + SoldApartments.objects.mark_inactive(inactive_sold_urls)
        for item in new_apartments:
            self._attempt_saving_item(item)
        for item in apartments_to_update:
            ap = self.model_for_url(item["origin_url"]).objects.get(
                bullettin_url=item["origin_url"]
            )
            self._attempt_saving_item(item, update=True, instance=ap)
        active_rented_urls, active_sold_urls = self.get_urls_by_type(self.active_urls)
        self._run_stats["total_active"] = RentApartment.objects.mark_active(
            active_rented_urls
        ) + SoldApartments.objects.mark_active(active_sold_urls)
        ApartmentDistanceEnricher(
            show_progress=False
        ).update_distance_data_for_apartments()
