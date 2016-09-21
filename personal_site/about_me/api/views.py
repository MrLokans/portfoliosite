from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from about_me.api.serializers import TechnologySerializer
from about_me.models import Project, Technology


class TechnologyListAPIView(ListAPIView):
    serializer_class = TechnologySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = 'name'
    search_fields = ['name', ]

    def get_queryset(self):
        qs = Technology.objects.all()
        return qs
