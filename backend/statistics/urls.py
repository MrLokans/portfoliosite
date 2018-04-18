from django.urls import path

from .api.views import (
    GetStatsPerHoursView,
)

urlpatterns = [
    path('per-hour/', GetStatsPerHoursView.as_view(), name='stats-per-hour'),
]
