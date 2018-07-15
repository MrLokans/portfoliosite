from django.views.generic import TemplateView
from django.views.generic import ListView

from .models import Technology, Project


class AboutMeView(ListView):

    queryset = Technology.objects.all()
    template_name = 'about_me.html'


class ProjectsListView(ListView):

    template_name = 'projects.html'
    queryset = Project.objects.fully_joined()


class ContactDetailsView(TemplateView):

    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        return {}


class ApartmentsStatisticsView(TemplateView):

    template_name = 'apartments_stats.html'
