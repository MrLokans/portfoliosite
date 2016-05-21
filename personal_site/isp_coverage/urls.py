from django.conf.urls import url

from .views import MapView


urlpatterns = [
    url(r'^providers$', MapView.as_view(), name='providers'),
]
