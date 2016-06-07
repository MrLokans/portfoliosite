import logging

from django.core.management.base import BaseCommand

from by_isp_coverage import ByflyParser, MTS_Parser, CSV_Exporter

from isp_coverage.models import Provider, ProviderCoordinate
from isp_coverage.views import MTS_CSV_FILE, BYFLY_CSV_FILE


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """Import internet coverage data and export it to CSV files."""

    def handle(self, *args, **kwargs):

        ProviderCoordinate.objects.all().delete()
        byfly_provider, _ = Provider.objects.get_or_create(name="byfly", url="http://byfly.by")
        mts_provider, _ = Provider.objects.get_or_create(name="mts", url="http://mts.by")
        unet_provider, _ = Provider.objects.get_or_create(name="unet", url="http://unet.by")

        byfly_parser = ByflyParser()
        mts_parser = MTS_Parser()
        # exporter = CSV_Exporter()

        logger.info("Obtaining data from byfly.")
        byfly_data = byfly_parser.get_points()
        logger.info("Saving data from byfly to database.")
        for point in byfly_data:
            coord = ProviderCoordinate.fromnamedtuple(point, byfly_provider)
            coord.save()

        logger.info("Obtaining data from mts.")
        mts_data = mts_parser.get_points()
        logger.info("Saving data from mts to database.")
        for point in mts_data:
            coord = ProviderCoordinate.fromnamedtuple(point, mts_provider)
            coord.save()

        # exporter.export_points(MTS_CSV_FILE, mts_data)
        # exporter.export_points(BYFLY_CSV_FILE, byfly_data)
