from django.urls import path

from .api.views import (
    AgentCheckView,
    ApartmentsListAPIView,
    ApartmentsStatsAPIView,
    PriceFluctuationsAPIView,
    DailyPriceFluctuationsAPIView,
)


app_name = "apartments_analyzer"

urlpatterns = [
    path("agents/<int:user_id>/", AgentCheckView.as_view(), name="agent-check"),
    path("", ApartmentsListAPIView.as_view(), name="apartments-list"),
    path("stats/", ApartmentsStatsAPIView.as_view(), name="apartments-stats"),
    path(
        "stats/fluctuations/",
        PriceFluctuationsAPIView.as_view(),
        name="price-fluctuations",
    ),
    path(
        "stats/fluctuations/daily/",
        DailyPriceFluctuationsAPIView.as_view(),
        name="daily-price-fluctuations",
    ),
]
