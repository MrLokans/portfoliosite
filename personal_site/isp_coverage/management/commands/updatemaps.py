import logging
from threading import Thread

from django.core.management.base import BaseCommand

from by_isp_coverage import ByflyParser, MTS_Parser, UNETParser, AtlantParser, CSV_Exporter

from isp_coverage.models import Provider, ProviderCoordinate
from isp_coverage.views import MTS_CSV_FILE, BYFLY_CSV_FILE


logger = logging.getLogger(__name__)


class CoordSaver(Thread):

    def __init__(self, parser):
        super().__init__()
        self.parser = parser

    def run(self):
        print("Obtaining data from {}".format(self.parser.PARSER_NAME))
        provider, _ = Provider.objects.get_or_create(name=ByflyParser.PARSER_NAME)
        data = self.parser.get_points()
        for point in data:
            coord = ProviderCoordinate.fromnamedtuple(point, provider)
            coord.save()


class Command(BaseCommand):
    help = """Import internet coverage data and export it to CSV files."""

    def handle(self, *args, **kwargs):

        ProviderCoordinate.objects.all().delete()

        byfly_parser = ByflyParser()
        mts_parser = MTS_Parser()
        unet_parser = UNETParser()
        atlant_parser = AtlantParser()
        # exporter = CSV_Exporter()

        parsers = [byfly_parser, mts_parser, atlant_parser, unet_parser]

        threads = [CoordSaver(p) for p in parsers]
        for t in threads:
            t.start()

        for t in threads:
            t.join()
