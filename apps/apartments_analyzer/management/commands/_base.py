import logging

import redis
from agent_spider.url_cache import DummyCache, RedisURLCache

from django.conf import settings
from django.core.management.base import CommandError

from agent_spider.run import SpiderLauncher

from apps.core.base_command import BaseSingletonCommand

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SUPPORTED_EXTENSIONS = ("json",)


class BaseParserCommand(BaseSingletonCommand):
    help = """Spider launching command."""

    def _url_cache_factory(self, django_settings):
        return DummyCache()

    def _generate_filename(self):
        return "bulletins.json"

    def _validate_filename(self, filename):
        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            raise CommandError(
                f'File "{filename}"" extension is not supported. '
                f"Supported extenstions: {SUPPORTED_EXTENSIONS}"
            )

    def _launch_spider(self, output_filename):
        overridden_settings = {
            "FEED_FORMAT": output_filename.split(".")[-1],
            "FEED_URI": output_filename,
            "SPIDER_LOADER_WARN_ONLY": True,
            "LOG_LEVEL": "ERROR",
            "LOG_STDOUT": False,
        }
        logger.info("Starting the apartment spider.")
        launcher = SpiderLauncher(
            local_settings=overridden_settings,
            url_cache=self._url_cache_factory(django_settings=settings)
        )
        launcher.run()

    def add_arguments(self, parser):
        parser.add_argument(
            "--filename", type=str, required=False, help="Output file for the parser."
        )
