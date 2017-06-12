from django.conf.urls import url

from apartments_analyzer.api.views import ApartmentsListAPIView


urlpatterns = [
    url(r'^$', ApartmentsListAPIView.as_view(), name="projects-list"),
]
