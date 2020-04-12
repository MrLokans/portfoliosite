from django.urls import path

from .api import views


app_name = "apartments_analyzer"

urlpatterns = [
    path("agents/<int:user_id>/", views.AgentCheckView.as_view(), name="agent-check"),
    path("search-areas/<int:contact_id>/", views.SearchAreasView.as_view(), name="search-regions"),
    path("", views.ApartmentsListAPIView.as_view(), name="apartments-list"),
    path("stats/", views.ApartmentsStatsAPIView.as_view(), name="apartments-stats"),
    path("stats/latest/", views.ApartmentsLatestStatsAPIView.as_view(), name="latest-stats"),
    path(
        "stats/fluctuations/",
        views.PriceFluctuationsAPIView.as_view(),
        name="price-fluctuations",
    ),
    path(
        "stats/fluctuations/daily/",
        views.DailyPriceFluctuationsAPIView.as_view(),
        name="daily-price-fluctuations",
    ),
]
