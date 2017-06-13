import json
import os
from typing import Dict, List, Set

from django.db import transaction

from apartments_analyzer.models import Apartment
from apartments_analyzer.api.serializers import ApartmentSerializer


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

    def save_apartments_data(self,
                             new_apartments,
                             inactive_urls: Set[str],
                             new_urls: Set[str]):
        with transaction.atomic():
            Apartment.objects.mark_inactive(inactive_urls)
            for item in new_apartments:
                ser = ApartmentSerializer(data=item)
                ser.is_valid()
                ser.save()
            Apartment.objects.mark_active(new_urls)

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
        new_apartments = (i for i in items
                          if i['origin_url'] in new_urls)

        self.save_apartments_data(new_apartments,
                                  inactive_urls,
                                  new_urls)
