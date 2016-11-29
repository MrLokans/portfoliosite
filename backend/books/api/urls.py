from django.conf.urls import url

from books.api.views import BookListAPIView, BookDetailAPIView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/', BookDetailAPIView.as_view(), name="list"),
    url(r'^$', BookListAPIView.as_view(), name="detail"),
]
