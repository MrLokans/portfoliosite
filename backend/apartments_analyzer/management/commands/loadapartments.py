import logging
import os
import json

from django.core.management.base import BaseCommand
from django.db import transaction


from apartments_analyzer.models import Apartment
from apartments_analyzer.api.serializers import ApartmentSerializer


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = """Load apartments data from JSON."""

    def load_from_json(self, filename):
        """
        Reads parsed JSON file and attempts
        to create database entries from it
        """
        if not os.path.exists(filename):
            raise ValueError(f'Filename {filename} does not exist.')
        with open(filename) as f:
            json_items = json.load(f)

        existing_apartments = Apartment.objects.all()
        existing_urls = set(ap.bullettin_url
                            for ap in existing_apartments)
        loaded_urls = set(i['origin_url']
                          for i in json_items)

        inactive_urls = existing_urls - loaded_urls
        active_urls = loaded_urls - inactive_urls
        new_urls = loaded_urls - existing_urls
        new_apartments = (i for i in json_items
                          if i['origin_url'] in new_urls)
        with transaction.atomic():
            Apartment.objects.mark_inactive(inactive_urls)
            for item in new_apartments:
                ser = ApartmentSerializer(data=item)
                ser.is_valid()
                ser.save()
            Apartment.objects.mark_active(new_urls)
            Apartment.objects.mark_active(active_urls)

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, required=True)

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        logger.error(f'Loading apartments data from file "{filename}".')
        self.load_from_json(filename)
