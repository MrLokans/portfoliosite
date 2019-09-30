from apps.apartments_analyzer import models
from apps.apartments_analyzer.management.commands import _base


class Command(_base.BaseParserCommand):
    help = """Remove existing parsed apartments."""

    def handle(self, *args, **kwargs):
        for model in (models.RentApartment, models.SoldApartments):
            model.objects.all().delete()
