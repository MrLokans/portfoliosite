import datetime
import json
import logging
import os
from typing import Dict, List, Set

from .api.serializers import ApartmentSerializer
from .models import Apartment, ApartmentScrapingResults

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ApartmentDataImporter(object):
    """
    Take care of importing apartment data into
    the database
    """
    __JSON_DATABASE_FIELD_MAP = {
        # JSON field: Corresponding DB model field
        'images': 'image_links',
        'origin_url': 'bullettin_url',
        'phones': 'user_phones',
        'user_url': 'author_url',
    }

    def __init__(self):
        self._reset_urls()

    def reset(self):
        self._reset_urls()

    def _reset_urls(self):
        self.inactive_urls = []
        self.active_urls = []
        self.invalid_urls = []

    def _map_field_names_to_internal_format(self, data: Dict) -> Dict:
        name_map = self.__JSON_DATABASE_FIELD_MAP
        output_data = {}
        for field_name, value in data.items():
            if field_name in name_map:
                output_data[name_map[field_name]] = value
            else:
                output_data[field_name] = value
        return output_data

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

    def _attempt_saving_item(self,
                             item_data: Dict,
                             stats: Dict,
                             update: bool = False,
                             instance=None):
        item_data = self._map_field_names_to_internal_format(item_data)
        item_data['description'] = self\
            ._clean_up_description(item_data['description'])
        serializer_args = {'data': item_data}
        processed_url = item_data['bullettin_url']
        if update:
            serializer_args.update({'instance': instance})
        ser = ApartmentSerializer(**serializer_args)
        if ser.is_valid():
            try:
                ser.save()
                stats['total_saved'] += 1
                if update:
                    stats['updated_items'] += 1
                else:
                    stats['new_items'] += 1
                self.active_urls.append(processed_url)
            except Exception:
                logger.exception("Error saving data %s.", ser.validated_data)
                stats['total_errors'] += 1
                self.invalid_urls.append(processed_url)
        else:
            logger.error('Invalid payload: %s', ser.errors)
            stats['total_errors'] += 1
            self.invalid_urls.append(processed_url)

    def _handle_database_sync(self,
                              new_apartments,
                              apartments_to_update,
                              inactive_urls: Set[str],
                              stats: Dict) -> Dict:
        stats['total_inactive'] = Apartment.objects.mark_inactive(inactive_urls)
        for item in new_apartments:
            self._attempt_saving_item(item, stats)
        for item in apartments_to_update:
            ap = Apartment.objects.get(bullettin_url=item['origin_url'])
            self._attempt_saving_item(item, stats,
                                      update=True, instance=ap)
        stats['total_active'] = Apartment.objects.mark_active(self.active_urls)
        return stats

    def save_apartments_data(self,
                             new_apartments,
                             apartments_to_update,
                             inactive_urls: Set[str]):
        scrape_stats = {
            'total_errors': 0,
            'total_active': 0,
            'total_inactive': 0,
            'total_saved': 0,
            'new_items': 0,
            'updated_items': 0,
            'error_message': "",
            'succeeded': True,
            'time_started': datetime.datetime.utcnow(),
            'time_finished': None,
            'invalid_urls': []
        }
        try:
            self._handle_database_sync(new_apartments,
                                       apartments_to_update,
                                       inactive_urls,
                                       scrape_stats)
        except Exception as exc:
            logger.exception('Error saving changes to the database.')
            scrape_stats['succeeded'] = False
            scrape_stats['error_message'] = str(exc)
        finally:
            scrape_stats['time_finished'] = datetime.datetime.utcnow()
            if self.invalid_urls:
                scrape_stats['succeeded'] = False
            scrape_stats['invalid_urls'] = self.invalid_urls
            stats = ApartmentScrapingResults(**scrape_stats)
            stats.save()
            self.reset()

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
        loaded_urls = set(i['origin_url'] for i in items)
        inactive_urls = existing_urls - loaded_urls
        new_urls = loaded_urls - existing_urls
        updated_urls = loaded_urls - new_urls
        new_apartments = (i for i in items
                          if i['origin_url'] in new_urls)
        apartments_to_update = (i for i in items
                                if i['origin_url'] in updated_urls)
        self.save_apartments_data(new_apartments,
                                  apartments_to_update,
                                  inactive_urls)
