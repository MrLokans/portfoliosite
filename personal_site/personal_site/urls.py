from django.conf.urls import include, url
from django.contrib import admin

from blog.views import LoginView, LogoutView, SignUpView, NewPost

urlpatterns = [
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('blog.urls')),
    # url(r'^$', HomeView.as_view(), name="home"),
    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^logout$', LogoutView.as_view(), name="logout"),
    url(r'^signup$', SignUpView.as_view(), name="signup"),
    url(r'^new-post$', NewPost.as_view(), name="new-post"),

]
