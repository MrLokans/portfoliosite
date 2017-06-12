from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny

from apartments_analyzer.api.serializers import ApartmentSerializer
from apartments_analyzer.models import Apartment


class ApartmentsListAPIView(ListAPIView):
    serializer_class = ApartmentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = (AllowAny, )
    ordering = '-price'
    search_fields = ['price', ]

    def get_queryset(self):
        qs = Apartment.objects.prefetch_related('images')
        return qs
