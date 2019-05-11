from django.conf import settings

from apps.apartments_analyzer.management.commands import _base
from apps.apartments_analyzer.services.search_results_reporter import SearchReporter


class Command(_base.BaseParserCommand):
    help = """
    Run search for user saved filters.
    """

    def handle(self, *args, **kwargs):
        SearchReporter.from_settings(settings).process_user_searches()
