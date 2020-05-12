import collections
from typing import Tuple

import jwt
from django.conf import settings
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.cache import cache_page

from apps.internal_users import models
from apps.apartments_analyzer import entities
from apps.apartments_analyzer.utils import construct_onliner_user_url
from apps.apartments_analyzer.models import (
    RentApartment,
    AreaOfInterest,
    PrecalculatedApartmentStats,
)
from apps.apartments_analyzer.permissions import TelegramAuthAccess
from apps.apartments_analyzer.api.serializers import (
    LatestStatsSerializer,
    StatsHistorySerializer,
    RentApartmentSerializer,
)
from apps.apartments_analyzer.services.telegram_auth import TelegramUserService
from apps.apartments_analyzer.services.stats_aggregator import (
    ApartmentsStatisticsAggregator,
)

from django.utils.decorators import method_decorator
from django.utils.functional import cached_property

AGENT_COUNT_THRESHOLD = 2


def data_representation_as_tuple(date_representation: str) -> Tuple:
    return tuple((int(date_part) for date_part in date_representation.split("-")))


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


class ApartmentsLatestStatsAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)

    serializer_class = LatestStatsSerializer

    def get_object(self):
        return PrecalculatedApartmentStats.objects.fetch_latest()


class ApartmentsStatsProgressAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None
    serializer_class = StatsHistorySerializer

    def get_queryset(self):
        return PrecalculatedApartmentStats.objects.latest_per_day(days_before=60)


class SearchAreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaOfInterest
        fields = (
            "uuid",
            "poly",
            "name",
        )


class SearchAreasView(ListAPIView):

    permission_classes = (TelegramAuthAccess,)
    serializer_class = SearchAreaListSerializer
    service = TelegramUserService.from_settings(settings)

    def get_queryset(self):
        search = self.service.get_search(self.request.telegram_user)
        return search.areas_of_interest.all()

    @method_decorator(cache_page(60 * 60 * 6))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


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
        data = collections.defaultdict(lambda: {"rooms": {}})
        for item in fluctuation_data:
            data[item["import_month"]]["rooms"][item["total_rooms"]] = item[
                "average_price"
            ]
        return [[item, value] for item, value in data.items()]

    @method_decorator(cache_page(60 * 60 * 10))
    def get(self, *args, **kwargs):
        return Response(
            self.as_response(
                ApartmentsStatisticsAggregator.prices_fluctuation_per_month()
            )
        )


class DailyPriceFluctuationsAPIView(APIView):
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
        data = collections.defaultdict(lambda: {"rooms": {}})

        for item in fluctuation_data:
            data[item["import_day"]]["rooms"][item["total_rooms"]] = item[
                "average_price"
            ]
        return [
            [item, value]
            for item, value in sorted(
                data.items(), key=lambda item: data_representation_as_tuple(item[0])
            )
        ]

    @method_decorator(cache_page(60 * 60 * 10))
    def get(self, *args, **kwargs):
        return Response(
            self.as_response(
                ApartmentsStatisticsAggregator.prices_fluctuation_per_day()
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


class TelegramAuthUserView(APIView):

    permission_classes = (AllowAny,)

    @cached_property
    def service(self):
        return TelegramUserService(settings.TELEGRAM_ACCESS_TOKEN)

    def authenticate_user(self, user_data: dict) -> models.TelegramUser:
        telegram_id = int(user_data["id"])
        get = user_data.get
        first_name, last_name, username = (
            get("first_name"),
            get("last_name"),
            get("username"),
        )
        internal_user = self.service.get_or_create_internal_user(
            entities.TelegramUserData(
                id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
        )
        return internal_user

    def auth_token_for_user(self, user: models.TelegramUser) -> str:
        return jwt.encode(
            {"telegram_id": user.telegram_id, "user_id": user.pk,},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

    def post(self, request, *args, **kwargs):
        user_data = request.data.copy()
        user_data.pop("format", "")
        self.service.verify_telegram_payload(user_data)
        user = self.authenticate_user(user_data=user_data)
        return Response(
            {
                "id": user.pk,
                "token": self.auth_token_for_user(user=user),
                "username": user.username,
            },
            status=status.HTTP_200_OK,
        )


class TelegramTokenVerifyView(APIView):

    permission_classes = (
        AllowAny,
        TelegramAuthAccess,
    )

    def get(self, request, *args, **kwargs):
        telegram_user = request.telegram_user
        return Response(
            {"id": telegram_user.pk, "username": telegram_user.username,},
            status=status.HTTP_200_OK,
        )
