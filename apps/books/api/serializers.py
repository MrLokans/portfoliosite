from rest_framework import serializers

from ..models import BookNote, Book


class BookNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookNote
        fields = [
            'id',
            'text',
        ]


class BookSerializer(serializers.ModelSerializer):
    notes = BookNoteSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'percentage',
            'rating',
            'notes'
        ]

    def create(self, validated_data):
        notes_data = validated_data.pop('notes')

        book = Book.objects.create(**validated_data)
        for note_data in notes_data:
            BookNote.objects.create(book=book, **note_data)
        return book

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.percentage = validated_data.get('percentage',
                                                 instance.percentage)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        notes = validated_data.get('notes', None)
        if notes is not None:
            pass
        return instance

    def get_notes(self, obj):
        notes = BookNote.objects.filter(book=obj)
        notes = BookNoteSerializer(notes, many=True).data
        return notes
