import logging
import os

from django.core.management.base import BaseCommand, CommandError

from apartments_analyzer.apartment_importer import ApartmentDataImporter
from apartments_analyzer.models import Apartment
from apartments_analyzer.api.serializers import ApartmentSerializer

from agent_spider.run import SpiderLauncher

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SUPPORTED_EXTENSIONS = ('json', )


class Command(BaseCommand):
    help = """Load apartments data from JSON."""

    def _generate_filename(self):
        # TODO: Add current date
        return 'bulletins.json'

    def _validate_filename(self, filename):
        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            raise CommandError(f'File "{filename}"" extension is not supported. '
                               f'Supported extenstions: {SUPPORTED_EXTENSIONS}')

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, required=False,
                            help='Output file for the parser.')

    def handle(self, *args, **kwargs):
        filename = kwargs['filename'] or self._generate_filename()
        self._validate_filename(filename)
        if os.path.exists(filename):
            logger.warning(f'File "{filename}" exists, attempting to remove.')
            os.unlink(filename)
        overridden_settings = {
            'FEED_FORMAT': filename.split('.')[-1],
            'FEED_URI': filename,
            'SPIDER_LOADER_WARN_ONLY': True,
            'LOG_LEVEL': 'INFO',
        }
        launcher = SpiderLauncher(local_settings=overridden_settings)
        launcher.run()
