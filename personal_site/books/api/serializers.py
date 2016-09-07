from rest_framework import serializers

from books.models import BookNote, Book


class BookNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookNote
        fields = [
            'id',
            'text',
        ]


class BookSerializer(serializers.ModelSerializer):
    notes = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'percentage',
            'rating',
            'notes'
        ]

    def get_notes(self, obj):
        notes = BookNote.objects.filter(book=obj)
        notes = BookNoteSerializer(notes, many=True).data
        return notes
