from django.conf.urls import patterns, url

from .views import MapView


urlpatterns = patterns(
    '',
    url(r'^providers$', MapView.as_view(), name='providers'),
)
