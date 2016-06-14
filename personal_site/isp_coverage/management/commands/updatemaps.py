import logging
from threading import Thread

from django.core.management.base import BaseCommand

from by_isp_coverage import (
    AtlantParser,
    ByflyParser,
    MTS_Parser,
    UNETParser
)

from isp_coverage.models import Provider, ProviderCoordinate


logger = logging.getLogger(__name__)


class CoordSaver(Thread):

    def __init__(self, parser):
        super().__init__()
        self.parser = parser

    def run(self):
        name = self.parser.PARSER_NAME
        print("Obtaining data from {}".format(name))
        provider, _ = Provider.objects.get_or_create(name=name)
        data = self.parser.get_points()
        for point in data:
            coord = ProviderCoordinate.fromnamedtuple(point, provider)
            coord.save()


class Command(BaseCommand):
    help = """Import internet coverage data and export it to CSV files."""

    def handle(self, *args, **kwargs):

        ProviderCoordinate.objects.all().delete()
        Provider.objects.all().delete()

        byfly_parser = ByflyParser()
        mts_parser = MTS_Parser()
        unet_parser = UNETParser()
        atlant_parser = AtlantParser()

        parsers = (atlant_parser, byfly_parser, mts_parser, unet_parser)

        threads = [CoordSaver(p) for p in parsers]
        for t in threads:
            t.start()

        for t in threads:
            t.join()
