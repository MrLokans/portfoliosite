from collections.__init__ import defaultdict
from typing import List, Dict

from django.db import models

from apps.books.models import BookNote, BookNameMapper


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
