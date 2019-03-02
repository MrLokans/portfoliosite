from django.urls import path

from .views import (
    AboutMeView,
    ContactDetailsView,
    ProjectsListView,
    ApartmentsStatisticsView,
)

app_name = "about_me"

urlpatterns = [
    path("", AboutMeView.as_view(), name="index"),
    path("projects", ProjectsListView.as_view(), name="projects"),
    path("contacts", ContactDetailsView.as_view(), name="contacts"),
    path("apartment-stats", ApartmentsStatisticsView.as_view(), name="analysis_stats"),
]
