from django.urls import path

from .api.views import (
    AgentCheckView,
    ApartmentsListAPIView,
)


app_name = 'apartments_analyzer'

urlpatterns = [
    path('agents/<int:user_id>/', AgentCheckView.as_view(), name="agent-check"),
    path('', ApartmentsListAPIView.as_view(), name="apartments-list"),
]
