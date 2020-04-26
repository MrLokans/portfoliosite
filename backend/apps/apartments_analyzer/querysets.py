import datetime
import functools
import operator

from django.db import models
from django.db.models import Q, When, Value, Case, functions, F
from django.utils import timezone

from apps.apartments_analyzer.enums import BulletinStatusEnum
from apps.apartments_analyzer.constants import SUBWAY_DISTANCES_FIELD


class PrecalculatedStatsQuerySet(models.QuerySet):
    def fetch_latest(self):
        return self.order_by('created_at').last()


class ApartmentsQueryset(models.QuerySet):

    _ROOM_ONLY_COUNT = 0
    _ROOM_TYPE_COUNT_MAPPING = {
        "Комната": _ROOM_ONLY_COUNT,
        "1-комнатная квартира": 1,
        "2-комнатная квартира": 2,
        "3-комнатная квартира": 3,
        "4-комнатная квартира": 4,
        "5-комнатная квартира": 5,
        "6-комнатная квартира": 6,
        "7-комнатная квартира": 7,
        "8-комнатная квартира": 8,
    }
    _UNKNOWN_ROOM_COUNT = -1

    def with_non_filled_subway_distance(self):
        return self.exclude(subway_distances__has_key=SUBWAY_DISTANCES_FIELD)

    def active(self):
        return self.filter(status=BulletinStatusEnum.ACTIVE.value)

    def inactive(self):
        return self.filter(status=BulletinStatusEnum.INACTIVE.value)

    def in_price_range(self, from_: int, to_: int):
        return self.filter(price_USD__gte=from_, price_USD__lte=to_)

    def with_rooms_equal_or_more(self, room_count: int):
        return self.filter(total_rooms__gte=room_count)

    def newer_than(self, diff: datetime.timedelta):
        now = timezone.now()
        return self.filter(last_active_parse_time__gt=now - diff)

    def in_areas(self, area_polygons):
        search_by_areas_filter = functools.reduce(
            operator.or_, [Q(location__within=poly) for poly in area_polygons]
        )
        return self.filter(search_by_areas_filter)

    def exclude_previous_search_results(self, previously_parsed_urls):
        return self.exclude(bullettin_url__in=previously_parsed_urls)

    def annotate_import_month(self):
        return self.annotate(
            import_month=functions.Concat(
                functions.ExtractYear("last_active_parse_time"),
                models.Value("-"),
                functions.ExtractMonth("last_active_parse_time"),
                output_field=models.CharField(),
            )
        )

    def annotate_import_day(self):
        return (
            self.annotate_import_month()
                .annotate(
                    import_day=functions.Concat(
                        F('import_month'),
                        models.Value("-"),
                        functions.ExtractDay("last_active_parse_time"),
                        output_field=models.CharField(),
                    )
        ))
