from django.conf.urls import url

from apartments_analyzer.api.views import (
    AgentCheckView,
    ApartmentsListAPIView,
)

urlpatterns = [
    url(r'^agents/(?P<user_id>\d+)/$',
        AgentCheckView.as_view(),
        name="agent-check"),
    url(r'^$', ApartmentsListAPIView.as_view(), name="projects-list"),
]
