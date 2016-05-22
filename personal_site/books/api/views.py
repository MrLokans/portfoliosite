from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from books.api.pagination import BookPageNumberPagination
from books.api.serializers import BookListSerializer
from books.models import Book


class BookListAPIView(ListAPIView):
    serializer_class = BookListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = 'title'
    # TODO: search by book's notes content
    search_fields = ['title', ]
    pagination_class = BookPageNumberPagination

    def get_queryset(self):
        qs = Book.objects.non_empty()
        return qs
