from datetime import timedelta
from typing import List, Tuple

from django.db.models import Count, Avg, F, Value, CharField, Min, Max
from django.db.models.functions import Concat, ExtractHour, ExtractWeekDay, ExtractMonth, ExtractYear
from django.utils import timezone

from .models import RentApartment, SoldApartments


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

    @staticmethod
    def get_price_metrics_for_last_n_days(day_count=30):
        later_than_days_ago = timedelta(days=day_count)
        after = timezone.now() - later_than_days_ago
        qs = (
            SoldApartments.objects
            .filter(last_active_parse_time__gte=after)
            .values('price_USD')
            .aggregate(
                average_price=Avg('price_USD'),
                min_price=Min('price_USD'),
                max_price=Max('price_USD')
            )
        )
        return [[key, value] for key, value in qs.items()]

    @staticmethod
    def get_average_square_meter_price_in_usd() -> List[Tuple[str, float]]:
        qs = (
            SoldApartments.objects
            .exclude(last_active_parse_time=None)
            .annotate(
                import_month=Concat(
                    ExtractYear('last_active_parse_time'), Value('-'), ExtractMonth('last_active_parse_time'),
                    output_field=CharField())
                )
            .values('import_month', )
            .annotate(
                average_price=Avg('price_USD'),
                average_square=Avg('total_area'),
            )
            .annotate(
                average_square_meter_price=F('average_price') / F('average_square')
            )
            .values('average_price', 'average_square', 'average_square_meter_price', 'import_month')
        )
        return [(item['import_month'], item['average_square_meter_price']) for item in qs]
