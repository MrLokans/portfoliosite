from rest_framework import serializers

from books.models import BookNote, Book


class BookListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
