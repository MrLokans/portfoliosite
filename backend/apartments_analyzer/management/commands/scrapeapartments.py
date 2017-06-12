import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError

import agent_spider


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = """Parse latest apartments data from onliner
    website and load it into the database"""

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        logger.info('Starting onliner apartments parsing.')
