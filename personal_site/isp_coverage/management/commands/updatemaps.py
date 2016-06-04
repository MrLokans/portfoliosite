from django.core.management.base import BaseCommand

from by_isp_coverage import ByflyParser, MTS_Parser, CSV_Exporter

from isp_coverage.views import MTS_CSV_FILE, BYFLY_CSV_FILE


class Command(BaseCommand):
    help = """Import internet coverage data and export it to CSV files."""

    def handle(self, *args, **kwargs):

        byfly_parser = ByflyParser()
        mts_parser = MTS_Parser()
        exporter = CSV_Exporter()

        byfly_data = byfly_parser.get_points()
        mts_data = mts_parser.get_points()

        exporter.export_points(MTS_CSV_FILE, mts_data)
        exporter.export_points(BYFLY_CSV_FILE, byfly_data)
