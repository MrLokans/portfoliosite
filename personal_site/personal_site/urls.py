from django.conf.urls import include, url
from django.contrib import admin

from blog.views import HomeView, AboutMeView, ProjectView, LoginView, LogoutView, SignUpView

urlpatterns = [
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^about_me$', AboutMeView.as_view(), name="about_me"),
    url(r'^projects$', ProjectView.as_view(), name="projects_list"),
    url(r'^projects/', include('isp_coverage.urls')),
    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^signup$', SignUpView.as_view(), name="signup"),
]
