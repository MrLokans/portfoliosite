from rest_framework.generics import ListAPIView

from books.api.serializers import BookListSerializer
from books.models import Book


class BookListAPIView(ListAPIView):
    serializer_class = BookListSerializer

    def get_queryset(self):
        qs = Book.objects.non_empty()
        return qs
