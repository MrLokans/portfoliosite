from apps.apartments_analyzer.management.commands import _base
from apps.apartments_analyzer.services.subway_distance_calculator import ApartmentDistanceEnricher


class Command(_base.BaseParserCommand):
    help = """
    Makes sure apartments in the db
    have information about relative
    database distance
    """

    def add_arguments(self, parser):
        parser.add_argument("--disable-progress", action='store_true')

    def handle(self, *args, **kwargs):
        disable_progress = kwargs['disable_progress']
        ApartmentDistanceEnricher(
            show_progress=not disable_progress
        ).update_distance_data_for_apartments()
