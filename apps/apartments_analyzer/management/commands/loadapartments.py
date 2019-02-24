from django.core.management.base import BaseCommand

from apps.apartments_analyzer.apartment_importer import ApartmentDataImporter


class Command(BaseCommand):
    help = """Load apartments data from JSON."""

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, required=True)

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        self.stdout.write(f'Loading apartments data from file "{filename}".\n')
        importer = ApartmentDataImporter()
        importer.load_from_json(filename)
