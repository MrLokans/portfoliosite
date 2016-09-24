from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from about_me.api.serializers import TechnologySerializer, ProjectSerializer
from about_me.models import Project, Technology


class TechnologyListAPIView(ListAPIView):
    serializer_class = TechnologySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = '-mastery_level'
    search_fields = ['name', ]

    def get_queryset(self):
        qs = Technology.objects.all()
        return qs


class ProjectListAPIView(ListAPIView):
    serializer_class = ProjectSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = 'title'
    search_fields = ['title', ]

    def get_queryset(self):
        qs = Project.objects.all()
        return qs
