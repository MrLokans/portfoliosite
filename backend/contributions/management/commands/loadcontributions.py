import logging

from django.core.management.base import (
    BaseCommand,
)
from django.db import transaction, IntegrityError
from contributions.models import Contribution
from contributions.services import ContributionObtainer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """Loads contributions data from github."""

    def add_arguments(self, parser):
        parser.add_argument('--username',
                            type=str,
                            default='MrLokans',
                            help='Github username')

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                obtainer = ContributionObtainer()
                Contribution.objects.all().delete()
                conts = obtainer.get_all_contributions(kwargs['username'])
                conts = [Contribution.from_contribution_object(c)
                         for c in set(conts)]
                Contribution.objects.bulk_create(conts)
        except IntegrityError as e:
            logger.exception("Database error.")
