from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.books.favorites import FavoritesService
from .pagination import BookPageNumberPagination
from .serializers import BookSerializer, FavoritesSerializer
from ..models import Book, Favorite


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = "title"
    search_fields = ("title", "notes__text")
    pagination_class = BookPageNumberPagination
    permission_classes = (AllowAny,)

    def get_queryset(self):
        qs = Book.objects.non_empty()
        return qs


class BookDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer

    permission_classes = (AllowAny,)

    def get_queryset(self):
        qs = Book.objects.non_empty()
        return qs


class FavoritesViewSet(viewsets.ModelViewSet):

    permission_classes = (AllowAny,)
    serializer_class = FavoritesSerializer
    queryset = Favorite.objects.order_by("added").all()

    @action(methods=["post"], detail=True)
    def book_to_favorites(self, request, pk):
        favorite = FavoritesService.add_book_to_favorites(pk)
        serialized = self.get_serializer_class()(instance=favorite)
        return Response(serialized.data)

    @action(methods=["post"], detail=True)
    def delete_book(self, request, pk):
        FavoritesService.remove_book_from_favorites(pk)
        return Response({})

    @action(methods=["post"], detail=True)
    def delete_note(self, request, pk):
        FavoritesService.remove_book_note_from_favorites(pk)
        return Response({})

    @action(methods=["post"], detail=True)
    def note_to_favorites(self, request, pk):
        favorite = FavoritesService.add_book_note_to_favorites(pk)
        serialized = self.get_serializer_class()(instance=favorite)
        return Response(serialized.data)
