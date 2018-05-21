import os
import json
from typing import Dict, List

from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class BookNote(models.Model):

    book = models.ForeignKey('Book', related_name='notes', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return 'BookNote(book={})'.format(self.book.title)


class BookManager(models.Manager):
    def non_empty(self, *args, **kwargs):
        qs = super().annotate(num_notes=models.Count('notes'))\
            .filter(num_notes__gt=0)
        return qs

    def load_new_entities(self, book_list: List[Dict]):
        self.get_queryset().delete()
        BookNote.objects.all().delete()
        book_objects = [
            self.model(title=b['title'], percentage=b['percentage'])
            for b in book_list
        ]
        # NOTE: here we rely on postgres behaviour to return the IDs of entities
        saved_books = self.bulk_create(book_objects, batch_size=400)
        created_notes = []
        for created_book, initial_book in zip(saved_books, book_list):
            created_book_id = created_book.id
            created_notes.extend([
                BookNote(book_id=created_book_id, text=n['text'])
                for n in initial_book['notes']
            ])
        BookNote.objects.bulk_create(created_notes, batch_size=400)


class Book(models.Model):

    author = models.CharField(max_length=300)
    title = models.CharField(max_length=200)
    percentage = models.IntegerField(default=0)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                        MaxValueValidator(5)])

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
