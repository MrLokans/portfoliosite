from django.conf.urls import url

from about_me.api.views import ProjectListAPIView

urlpatterns = [
    url(r'^$', ProjectListAPIView.as_view(), name="projects-list"),
]
