from django.conf.urls import url

from books.api.views import BookListAPIView

urlpatterns = [
    url(r'^$', BookListAPIView.as_view(), name="list"),
]
