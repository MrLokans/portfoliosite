import datetime
import json
import logging
import os
from typing import Dict, List, Set

from django.db import transaction, IntegrityError

from apartments_analyzer.models import Apartment, ApartmentScrapingResults
from apartments_analyzer.api.serializers import ApartmentSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ApartmentDataImporter(object):
    """
    Take care of importing apartment data into
    the database
    """

    def _get_existing_apartment_urls(self) -> Set[str]:
        """
        Gets list of apartment URLs already
        persisted to the database.
        """
        existing_apartments = (
            Apartment.objects
            .values_list('bullettin_url', flat=True)
        )
        return set(existing_apartments)

    def _clean_up_description(self, text: List[str]) -> str:
        joined_text = " ".join(text).replace('\n', ' ')
        placed_pos = joined_text.find('Размещено')
        if placed_pos != -1:
            joined_text = joined_text[:placed_pos]
        return joined_text or ''

    def _handle_database_sync(self,
                              new_apartments,
                              apartments_to_update,
                              inactive_urls: Set[str],
                              new_urls: Set[str],
                              stats: Dict) -> Dict:
        """
        :raises IntegrityError:
        """
        with transaction.atomic():
            stats['total_inactive'] = Apartment.objects.mark_inactive(inactive_urls)
            for item in new_apartments:
                item['description'] = self._clean_up_description(item['description'])
                ser = ApartmentSerializer(data=item)
                if ser.is_valid():
                    ser.save()
                    stats['total_saved'] += 1
                else:
                    logger.error('Error saving apartment data: %s', ser.errors)
                    stats['total_errors'] += 1
            # TODO: refactor and remove code duplication
            for item in apartments_to_update:
                item['description'] = self._clean_up_description(item['description'])
                ap = Apartment.objects.get(bullettin_url=item['origin_url'])
                ser = ApartmentSerializer(instance=ap, data=item)
                if ser.is_valid():
                    ser.save()
                    stats['total_saved'] += 1
                else:
                    logger.error('Error saving apartment data: %s', ser.errors)
                    stats['total_errors'] += 1
            stats['total_active'] = Apartment.objects.mark_active(new_urls)

    def save_apartments_data(self,
                             new_apartments,
                             apartments_to_update,
                             inactive_urls: Set[str],
                             new_urls: Set[str]):
        scrape_stats = {
            'total_errors': 0,
            'total_active': 0,
            'total_inactive': 0,
            'total_saved': 0,
            'error_message': "",
            'succeeded': True,
            'time_started': datetime.datetime.utcnow(),
            'time_finished': None,
        }
        try:
            self._handle_database_sync(new_apartments,
                                       apartments_to_update,
                                       inactive_urls, new_urls,
                                       scrape_stats)
        except Exception as exc:
            logger.exception('Error saving changes to the database.')
            scrape_stats['succeeded'] = False
            scrape_stats['error_message'] = str(exc)
        finally:
            scrape_stats['time_finished'] = datetime.datetime.utcnow()
            stats = ApartmentScrapingResults(**scrape_stats)
            stats.save()

    def load_from_json(self, filename: str):
        """
        Reads parsed JSON file and attempts
        to create database entries from it
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f'Filename {filename} does not exist.')
        with open(filename) as fd:
            json_items = json.load(fd)
        self.load_from_serialized_values(json_items)

    def load_from_serialized_values(self, items: List[Dict]):
        existing_urls = self._get_existing_apartment_urls()
        loaded_urls = set(i['origin_url']
                          for i in items)
        inactive_urls = existing_urls - loaded_urls
        new_urls = loaded_urls - existing_urls
        updated_urls = loaded_urls - new_urls
        new_apartments = (i for i in items
                          if i['origin_url'] in new_urls)
        apartments_to_update = (i for i in items
                                if i['origin_url'] in updated_urls)

        self.save_apartments_data(new_apartments,
                                  apartments_to_update,
                                  inactive_urls,
                                  new_urls)
