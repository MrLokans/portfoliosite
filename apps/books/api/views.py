from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny

from .pagination import BookPageNumberPagination
from .serializers import BookSerializer
from ..models import Book


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = 'title'
    # TODO: search by book's notes content
    search_fields = ['title', ]
    pagination_class = BookPageNumberPagination
    permission_classes = (AllowAny, ) 

    def get_queryset(self):
        qs = Book.objects.non_empty()
        return qs


class BookDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = Book.objects.non_empty()
        return qs
