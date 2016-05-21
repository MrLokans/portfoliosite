from django.conf.urls import include, url

from .views import HomeView, AboutMeView, ProjectView, BookListView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='index'),
    url(r'about_me$', AboutMeView.as_view(), name="about_me"),
    url(r'projects$', ProjectView.as_view(), name="projects_list"),
    url(r'projects/', include('isp_coverage.urls')),
    url(r'books$', BookListView.as_view(), name="book-list"),
]
