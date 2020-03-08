import collections
from datetime import timedelta
from typing import List, Tuple

from django.db import models
from django.db.models import functions
from django.utils import timezone

from apps.apartments_analyzer.models import RentApartment, SoldApartments


class ApartmentsStatisticsAggregator:
    @staticmethod
    def get_hour_aggregated_stats() -> List[Tuple[int, int]]:
        qs = (
            RentApartment.objects.exclude(last_active_parse_time=None)
            .values("last_active_parse_time")
            .annotate(current_hour=functions.ExtractHour("last_active_parse_time"))
            .values("current_hour")
            .annotate(count=models.Count("current_hour"))
        )

        return sorted(
            [(item["current_hour"], item["count"]) for item in qs], key=lambda t: t[0]
        )

    @staticmethod
    def get_weekday_aggregated_stats() -> List[Tuple[int, int]]:
        qs = (
            RentApartment.objects.exclude(last_active_parse_time=None)
            .values("last_active_parse_time")
            .annotate(
                current_weekday=functions.ExtractWeekDay("last_active_parse_time")
            )
            .values("current_weekday")
            .annotate(count=models.Count("current_weekday"))
        )
        return sorted(
            [(item["current_weekday"], item["count"]) for item in qs],
            key=lambda t: t[0],
        )

    @staticmethod
    def get_price_metrics_for_last_n_days(day_count=30):
        later_than_days_ago = timedelta(days=day_count)
        after = timezone.now() - later_than_days_ago
        qs = (
            SoldApartments.objects.filter(last_active_parse_time__gte=after)
            .values("price_USD")
            .aggregate(
                average_price=models.Avg("price_USD"),
                min_price=models.Min("price_USD"),
                max_price=models.Max("price_USD"),
            )
        )
        return [[key, value] for key, value in qs.items()]

    @staticmethod
    def get_average_square_meter_price_in_usd() -> List[Tuple[str, float]]:
        qs = (
            SoldApartments.objects.exclude(last_active_parse_time=None)
            .annotate(
                import_month=functions.Concat(
                    functions.ExtractYear("last_active_parse_time"),
                    models.Value("-"),
                    functions.ExtractMonth("last_active_parse_time"),
                    output_field=models.CharField(),
                )
            )
            .values("import_month")
            .annotate(
                average_price=models.Avg("price_USD"),
                average_square=models.Avg("total_area"),
            )
            .annotate(
                average_square_meter_price=models.F("average_price")
                / models.F("average_square")
            )
            .values(
                "average_price",
                "average_square",
                "average_square_meter_price",
                "import_month",
            )
        )
        return [
            (item["import_month"], item["average_square_meter_price"]) for item in qs
        ]

    @staticmethod
    def prices_fluctuation_per_month() -> List:
        """
        Returns price changes on a monthly basis
        from the beginning of parsing towards the current day.
        """
        return (
            RentApartment.objects.exclude(last_active_parse_time=None)
            .annotate_room_count()
            .annotate(
                import_month=functions.Concat(
                    functions.ExtractYear("last_active_parse_time"),
                    models.Value("-"),
                    functions.ExtractMonth("last_active_parse_time"),
                    output_field=models.CharField(),
                )
            )
            .annotate(
                average_price=models.Window(
                    expression=models.Avg("price_USD"),
                    partition_by=[models.F("import_month"), models.F("room_count")],
                )
            )
            .values("import_month", "room_count", "average_price")
            .distinct("import_month", "room_count")
        )
