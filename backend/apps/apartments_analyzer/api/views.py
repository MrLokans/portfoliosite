import collections

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.apartments_analyzer.services.stats_aggregator import (
    ApartmentsStatisticsAggregator,
)
from .serializers import RentApartmentSerializer
from ..models import RentApartment
from ..utils import construct_onliner_user_url


AGENT_COUNT_THRESHOLD = 2


class ApartmentsListAPIView(ListAPIView):
    serializer_class = RentApartmentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = (AllowAny,)
    ordering = "-price"
    search_fields = ["price"]

    def get_queryset(self):
        qs = RentApartment.objects.prefetch_related("images")
        return qs


class ApartmentsStatsAPIView(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60 * 60 * 10))
    def get(self, *args, **kwargs):
        stats = {}
        stats["by_hour"] = ApartmentsStatisticsAggregator.get_hour_aggregated_stats()
        stats[
            "average_square_meter_price"
        ] = ApartmentsStatisticsAggregator.get_average_square_meter_price_in_usd()
        stats[
            "by_weekday"
        ] = ApartmentsStatisticsAggregator.get_weekday_aggregated_stats()
        return Response(stats)


class PriceFluctuationsAPIView(APIView):
    permission_classes = (AllowAny,)

    def as_response(self, fluctuation_data):
        """
        The stats are also subdivided for the number of rooms
        as the metric that has the most effect on the price.

        Sample response:
        [
           ['2019-08', {'rooms': {'1': 100.0]}}],
           ...
        ]
        """
        months = collections.defaultdict(lambda: {"rooms": {}})
        for item in fluctuation_data:
            months[item["import_month"]]["rooms"][item["room_count"]] = item[
                "average_price"
            ]
        return [[item, value] for item, value in months.items()]

    @method_decorator(cache_page(60 * 60 * 10))
    def get(self, *args, **kwargs):
        return Response(
            self.as_response(
                ApartmentsStatisticsAggregator.prices_fluctuation_per_month()
            )
        )


class AgentCheckView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Checks whether the given user id belongs
        to the agent and also returns a list
        of bullettins
        """
        user_id = kwargs["user_id"]
        user_url = construct_onliner_user_url(user_id)
        apartment_urls = RentApartment.objects.filter(author_url=user_url).values_list(
            "bullettin_url", flat=True
        )
        apartment_urls = set(apartment_urls)
        if len(apartment_urls) <= AGENT_COUNT_THRESHOLD:
            is_agent_probability = 0
        else:
            is_agent_probability = 100
        payload = {
            "is_agent_probability": is_agent_probability,
            "posts": apartment_urls,
        }
        return Response(payload, status=status.HTTP_200_OK)
