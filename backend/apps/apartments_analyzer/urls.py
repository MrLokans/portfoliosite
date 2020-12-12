from django.urls import path

from .api import views


app_name = "apartments_analyzer"

urlpatterns = [
    path("agents/<int:user_id>/", views.AgentCheckView.as_view(), name="agent-check"),
    path("search-areas/", views.SearchAreasView.as_view(), name="search-regions"),
    path("", views.ApartmentsListAPIView.as_view(), name="apartments-list"),
    path("stats/", views.ApartmentsStatsAPIView.as_view(), name="apartments-stats"),
    path("stats/latest/", views.ApartmentsLatestStatsAPIView.as_view(), name="latest-stats"),
    path("stats/history/", views.ApartmentsStatsProgressAPIView.as_view(), name="latest-stats"),
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
    path(
        "stats/fluctuations/square-meter-price/monthly/",
        views.SquareMeterMonthlyPriceFluctuationsAPIView.as_view(),
        name="monthly-square-meter-price-fluctuations",
    ),
    # TODO: find a better place
    path(
        "telegram-login/",
        views.TelegramAuthUserView.as_view(),
        name="telegram-login"
    ),
    path(
        "verify-telegram-token/",
        views.TelegramTokenVerifyView.as_view(),
        name="telegram-verify"
    )
]
