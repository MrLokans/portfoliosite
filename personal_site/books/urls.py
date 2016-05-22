from django.conf.urls import url

from books.views import BookListView


urlpatterns = [
    url(r'books$', BookListView.as_view(), name="book-list"),
]
