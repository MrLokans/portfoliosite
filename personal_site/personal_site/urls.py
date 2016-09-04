from django.conf.urls import include, url
from django.contrib import admin

from blog.views import LoginView, LogoutView, SignUpView, NewPost

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('blog.urls')),
    url(r'^', include('books.urls')),
    url(r'^markdownx/', include('markdownx.urls')),
    # url(r'^$', HomeView.as_view(), name="home"),
    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^logout$', LogoutView.as_view(), name="logout"),
    url(r'^signup$', SignUpView.as_view(), name="signup"),
    url(r'^new-post$', NewPost.as_view(), name="new-post"),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/books/', include('books.api.urls', namespace='books-api')),
    url(r'^api/blog/', include('blog.api.urls', namespace='blog-api')),
]
