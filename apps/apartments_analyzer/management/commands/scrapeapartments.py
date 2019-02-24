import os

from apps.apartments_analyzer.apartment_importer import ApartmentDataImporter
from apps.apartments_analyzer.management.commands import _base


class Command(_base.BaseParserCommand):
    help = """
    Runs the apartments data spider, collects
    the data into the file and syncs it
    with the actual database.
    """

    def _sync_changes_to_database(self, filename):
        """
        Read aparatments data from the output file
        and sync it with the latest database state.
        """
        importer = ApartmentDataImporter()
        importer.load_from_json(filename)

    def handle(self, *args, **kwargs):
        filename = kwargs['filename'] or self._generate_filename()
        self._validate_filename(filename)
        if os.path.exists(filename):
            self.stdout.write(f'File "{filename}" exists, attempting to remove.\n')
            os.unlink(filename)
        self._launch_spider(filename)
        self._sync_changes_to_database(filename)
