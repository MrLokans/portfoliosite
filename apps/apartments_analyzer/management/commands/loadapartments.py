import logging

from django.core.management.base import BaseCommand

from apps.apartments_analyzer.apartment_importer import ApartmentDataImporter


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = """Load apartments data from JSON."""

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, required=True)

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        logger.info(f'Loading apartments data from file "{filename}".')
        importer = ApartmentDataImporter()
        importer.load_from_json(filename)
