from collections import defaultdict
from typing import Dict, List

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.functional import cached_property


class BookNameMapper(models.Model):
    incoming_book_name = models.CharField(max_length=200)
    output_title = models.CharField(max_length=200)
    output_author = models.CharField(max_length=200)

    def __str__(self):
        return "BookMap({})".format(self.incoming_book_name)


class BookNote(models.Model):

    book = models.ForeignKey("Book", related_name="notes", on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return "BookNote(book={})".format(self.book.proper_title)


class BookManager(models.Manager):
    def non_empty(self, *args, **kwargs):
        qs = super().annotate(num_notes=models.Count("notes")).filter(num_notes__gt=0)
        return qs

    def load_new_entities(self, book_list: List[Dict]):
        book_list = self.deduplicate_book_list(book_list)
        existing_titles = set(
            self.get_queryset().values_list("original_title", flat=True)
        )
        updated_books = [b for b in book_list if b["title"] in existing_titles]
        new_books = [b for b in book_list if b["title"] not in existing_titles]

        for book in updated_books:
            db_book = self.get_queryset().get(original_title=book["title"])
            db_book.notes.all().delete()
            db_book.number_of_pages = book["pages"]
            db_book.percentage = book["percentage"]
            db_book.save()
            BookNote.objects.bulk_create(
                [
                    self.preprocess_book_note(BookNote(book=db_book, text=n["text"]))
                    for n in book["notes"]
                ]
            )

        for book in new_books:
            db_book = self.model(
                original_title=book["title"],
                percentage=book["percentage"],
                number_of_pages=book["pages"],
            )
            db_book.save()
            BookNote.objects.bulk_create(
                [
                    self.preprocess_book_note(BookNote(book=db_book, text=n["text"]))
                    for n in book["notes"]
                ]
            )
        self.perform_name_translation()

    def preprocess_book_note(self, note: BookNote) -> BookNote:
        note.text = note.text.replace("<BR><BR>", "\n")
        note.text = note.text.replace("<BR>", "\n")
        note.text = note.text.strip()
        return note

    def deduplicate_book_list(self, book_list: List[Dict]) -> List[Dict]:
        """
        Removes duplicates of books, getting
        the instance with more notes or with a bigger
        percentage.
        """
        output_books = []
        deduplicated_books = defaultdict(lambda: [0, []])
        for book in book_list:
            deduplicated_books[book["title"]][0] += 1
            deduplicated_books[book["title"]][1].append(book)
        for _, (book_count, books) in deduplicated_books.items():
            if book_count == 1:
                output_books.append(books[0])
                continue

            output_books.append(self.__deduplicate(books))
        return output_books

    def perform_name_translation(self):
        all_books = self.get_queryset().all().only("original_title")
        existing_mappings = {
            m[0]: (m[1], m[2])
            for m in BookNameMapper.objects.values_list(
                "incoming_book_name", "output_title", "output_author"
            )
        }
        for book in all_books:
            if book.original_title in existing_mappings:
                title, author = existing_mappings[book.original_title]
                book.author = author
                book.title = title
                book.save(update_fields=["author", "title"])

    def __deduplicate(self, books: List[Dict]) -> Dict:
        max_notes = max(books, key=lambda b: len(b["notes"]))
        min_notes = min(books, key=lambda b: len(b["notes"]))
        if max_notes != min_notes:
            return max_notes
        return max(books, key=lambda b: b["percentage"])


class Book(models.Model):

    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200, default="")
    original_title = models.CharField(max_length=200)
    percentage = models.IntegerField(default=0)
    rating = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    number_of_pages = models.IntegerField(default=0)

    objects = BookManager()

    def __str__(self):
        return "<Book {}>".format(self.proper_title)

    @cached_property
    def proper_title(self) -> str:
        if self.author and self.title:
            return "{} - {}".format(self.author, self.title)
        return self.original_title

    def get_related_notes(self):
        return self.booknote_set.all()

    def is_empty(self):
        return self.booknote_set.count() == 0


class Favorite(models.Model):
    note = models.TextField(help_text="Why it is special", default="")
    added = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
