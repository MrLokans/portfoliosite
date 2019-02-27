from django.test import TestCase

from apps.books.favorites import FavoritesService
from apps.books.models import Book, Favorite, BookNote


class FavoritesServiceTestCase(TestCase):
    def test_adding_new_favorite_for_book_creates_favorite(self):
        b = Book(title="test")
        b.save()
        self.assertEqual(Favorite.objects.count(), 0)
        FavoritesService.add_book_to_favorites(b.id, reason="I liked that one")
        self.assertEqual(Favorite.objects.count(), 1)

    def test_adding_new_favorite_for_book_note_creates_favorite(self):
        b = Book(title="test")
        b.save()
        note = BookNote(text="Hello!", book=b)
        note.save()
        self.assertEqual(Favorite.objects.count(), 0)
        FavoritesService.add_book_note_to_favorites(note.id, reason="I liked that one")
        self.assertEqual(Favorite.objects.count(), 1)
