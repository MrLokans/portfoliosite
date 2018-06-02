import os
import json
from collections import defaultdict
from typing import Dict, List

from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator


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
        book_list = self.deduplicate_book_list(book_list)
        existing_titles = set(self.get_queryset().values_list('title', flat=True))
        updated_books = [b for b in book_list if b['title'] in existing_titles]
        new_books = [b for b in book_list if b['title'] not in existing_titles]

        for book in updated_books:
            db_book = self.get_queryset().get(title=book['title'])
            db_book.notes.all().delete()
            db_book.number_of_pages = book['pages']
            db_book.percentage = book['percentage']
            db_book.save()
            BookNote.objects.bulk_create([BookNote(book=db_book, text=n['text']) for n in book['notes']])

        for book in new_books:
            db_book = self.model(
                title=book['title'],
                percentage=book['percentage'],
                number_of_pages=book['pages']
            )
            db_book.save()
            BookNote.objects.bulk_create([BookNote(book=db_book ,text=n['text']) for n in book['notes']])

    def deduplicate_book_list(self, book_list: List[Dict]) -> List[Dict]:
        """
        Removes duplicates of books, getting
        the instance with more notes or with a bigger
        percentage.
        """
        output_books = []
        deduplicated_books = defaultdict(lambda: [0, []])
        for book in book_list:
            deduplicated_books[book['title']][0] += 1
            deduplicated_books[book['title']][1].append(book)
        for book_title, (book_count, books) in deduplicated_books.items():
            if book_count == 1:
                output_books.append(books[0])
                continue

            output_books.append(self.__deduplicate(books))
        return output_books

    def __deduplicate(self, books: List[Dict]) -> Dict:
        max_notes, min_notes = max(books, key=lambda b: len(b['notes'])),  min(books, key=lambda b: len(b['notes']))
        if max_notes != min_notes:
            return max_notes
        return max(books, key=lambda b: b['percentage'])


class Book(models.Model):

    author = models.CharField(max_length=300)
    title = models.CharField(max_length=200)
    percentage = models.IntegerField(default=0)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                        MaxValueValidator(5)])
    number_of_pages = models.IntegerField(default=0)

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
