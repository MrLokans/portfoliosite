from django.conf.urls import include, url
from django.contrib import admin

from blog.views import LoginView, LogoutView, SignUpView

urlpatterns = [
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('blog.urls')),
    # url(r'^$', HomeView.as_view(), name="home"),
    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^signup$', SignUpView.as_view(), name="signup"),

]
