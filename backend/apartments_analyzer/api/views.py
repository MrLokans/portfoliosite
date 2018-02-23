from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apartments_analyzer.api.serializers import ApartmentSerializer
from apartments_analyzer.models import Apartment
from apartments_analyzer.utils import construct_onliner_user_url


AGENT_COUNT_THRESHOLD = 2


class ApartmentsListAPIView(ListAPIView):
    serializer_class = ApartmentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = (AllowAny, )
    ordering = '-price'
    search_fields = ['price', ]

    def get_queryset(self):
        qs = Apartment.objects.prefetch_related('images')
        return qs


class AgentCheckView(APIView):

    def get(self, request, *args, **kwargs):
        """
        Checks whether the given user id belongs
        to the agent and also returns a list
        of bullettins
        """
        user_id = kwargs['user_id']
        user_url = construct_onliner_user_url(user_id)
        apartment_urls = Apartment.objects\
            .filter(author_url=user_url)\
            .values_list('bullettin_url', flat=True)
        apartment_urls = set(apartment_urls)
        if len(apartment_urls) <= AGENT_COUNT_THRESHOLD:
            is_agent_probability = 0
        else:
            is_agent_probability = 100
        payload = {
            "is_agent_probability": is_agent_probability,
            "posts": apartment_urls
        }
        return Response(payload, status=status.HTTP_200_OK)
