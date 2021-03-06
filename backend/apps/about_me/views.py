from django.views.generic import TemplateView
from django.views.generic import ListView

from apps.about_me.models import Technology, Project


class AboutMeView(ListView):

    queryset = Technology.objects.all()
    template_name = "about_me.html"


class ProjectsListView(ListView):

    template_name = "projects.html"
    queryset = Project.objects.fully_joined()


class ApartmentsStatisticsView(TemplateView):

    template_name = "apartments_stats.html"
