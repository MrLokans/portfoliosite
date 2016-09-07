import os
import json

from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class BookManager(models.Manager):
    def non_empty(self, *args, **kwargs):
        qs = super().annotate(num_notes=models.Count('notes'))\
            .filter(num_notes__gt=0)
        return qs


class Book(models.Model):

    author = models.CharField(max_length=300)
    title = models.CharField(max_length=200, unique=True)
    percentage = models.IntegerField(default=0)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                        MaxValueValidator(5)])
    # TODO: tag should be turned into generic foreign key
    # tag = models.ManyToManyField(Tag)

    objects = BookManager()

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

    @staticmethod
    def from_dict(book_dict):
        title = book_dict['title']
        percentage = book_dict['percentage']

        db_book = Book(title=title, percentage=percentage)
        db_book.save()

        notes = book_dict.get('notes', [])
        for note in notes:
            note_obj = BookNote(text=note['text'], book=db_book)
            note_obj.save()
        db_book.save()

    def get_related_notes(self):
        return self.booknote_set.all()

    def is_empty(self):
        return self.booknote_set.count() == 0


class BookNote(models.Model):

    book = models.ForeignKey('Book', related_name='notes')
    text = models.TextField()
