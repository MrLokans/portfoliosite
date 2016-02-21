import os
import json

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from tinymce import models as tinymce_models


class Tag(models.Model):
    value = models.CharField(max_length=60)


class Post(models.Model):
    # TODO: turn to slug field
    title = models.CharField(max_length=200)
    text = tinymce_models.HTMLField()
    # Deal withmany to many fields
    tags = models.ManyToManyField(Tag)


class Book(models.Model):

    author = models.CharField(max_length=300)
    title = models.CharField(max_length=200)
    percentage = models.IntegerField(default=0)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return '<Book {}>'.format(self.title)

    @staticmethod
    def from_json(json_path):
        assert os.path.exists(json_path)
        data = []
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for book in data.get('books', []):
            db_book = Book(title=book['title'], percentage=book['percentage'])
            db_book.save()
            for note in book.get('notes', []):
                note = BookNote(text=note['text'], book=db_book)
                note.save()
            db_book.save()

    @classmethod
    def non_empty(cls):
        return cls.objects.exclude(booknote=None)

    def get_related_notes(self):
        return self.booknote_set.all()

    def is_empty(self):
        return self.booknote_set.count() == 0


class BookNote(models.Model):

    book = models.ForeignKey('Book')
    text = models.TextField()
