from django.conf.urls import url

from about_me.api.views import TechnologyListAPIView

urlpatterns = [
    url(r'^$', TechnologyListAPIView.as_view(), name="technology-list"),
]
