import logging

from django.core.management.base import BaseCommand

from apps.apartments_analyzer.deduplicator import Deduplicator
from apps.apartments_analyzer.models import Apartment

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = """Deduplicates data in the database."""

    def handle(self, *args, **kwargs):
        deduplicator = Deduplicator(Apartment, 'bullettin_url')
        deduplicator.remove_duplicate_apartments()
