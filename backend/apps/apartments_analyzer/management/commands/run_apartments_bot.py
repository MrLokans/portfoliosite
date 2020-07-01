import logging

from django.conf import settings as django_settings
from django.core.management.base import BaseCommand

from apps.apartments_analyzer.telegram_bot.interaction import ApartmentReporterBot
from apps.apartments_analyzer.telegram_bot.repository import TelegramSearchRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)




class Command(BaseCommand):
    def handle(self, *args, **options):
        bot = ApartmentReporterBot(
            logger=logger,
            repo=TelegramSearchRepository(),
            access_token=django_settings.TELEGRAM_ACCESS_TOKEN,
        )
        bot.run()
