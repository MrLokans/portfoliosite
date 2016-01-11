from django.conf.urls import patterns, include, url

from .views import BlogIndex, BlogDetail, BooksIndex

urlpatterns = patterns(
    '',
    url(r'^$', BlogIndex.as_view(), name='index'),
    url(r'^/books$', BooksIndex.as_view(), name='books'),
)
