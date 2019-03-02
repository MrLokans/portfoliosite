from typing import List, Tuple

from django.db.models import Count
from django.db.models.functions import ExtractHour, ExtractWeekDay

from .models import RentApartment


class ApartmentsStatisticsAggregator:
    @staticmethod
    def get_hour_aggregated_stats() -> List[Tuple[int, int]]:
        qs = (
            RentApartment.objects.values("created_at")
            .annotate(current_hour=ExtractHour("created_at"))
            .values("current_hour")
            .annotate(count=Count("current_hour"))
        )

        return sorted(
            [(item["current_hour"], item["count"]) for item in qs], key=lambda t: t[0]
        )

    @staticmethod
    def get_weekday_aggregated_stats() -> List[Tuple[int, int]]:
        qs = (
            RentApartment.objects.values("created_at")
            .annotate(current_weekday=ExtractWeekDay("created_at"))
            .values("current_weekday")
            .annotate(count=Count("current_weekday"))
        )
        return sorted(
            [(item["current_weekday"], item["count"]) for item in qs],
            key=lambda t: t[0],
        )
