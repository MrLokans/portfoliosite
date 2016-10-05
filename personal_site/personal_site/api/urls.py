from django.conf.urls import url

from blog.api.views import PostListAPIView, PostDetailsAPIView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/', PostDetailsAPIView.as_view(), name='detail'),
    url(r'^$', PostListAPIView.as_view(), name="list"),
]
