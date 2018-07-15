import logging
import os

from apps.apartments_analyzer.management.commands import _base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(_base.BaseParserCommand):
    help = """Load apartments data from JSON."""

    def handle(self, *args, **kwargs):
        filename = kwargs['filename'] or self._generate_filename()
        self._validate_filename(filename)
        if os.path.exists(filename):
            logger.warning(f'File "{filename}" exists, attempting to remove.')
            os.unlink(filename)
        self._launch_spider(filename)
