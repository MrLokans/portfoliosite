from django.conf.urls import url

from .views import MapView, get_provider_dots


urlpatterns = [
    url(r'^providers$', MapView.as_view(), name='providers'),
    url(r'^providers-api$', get_provider_dots, name='api'),
]
