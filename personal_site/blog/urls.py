from django.conf.urls import url

from .views import HomeView, ProjectView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    # url(r'about_me$', AboutMeView.as_view(), name="about_me"),
    url(r'projects$', ProjectView.as_view(), name="projects_list"),
]
