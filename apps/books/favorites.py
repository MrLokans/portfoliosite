from django.contrib.contenttypes.models import ContentType

from apps.books.models import Book, BookNote, Favorite


class FavoritesService:

    @classmethod
    def remove_book_from_favorites(cls, book_id: int):
        Favorite.objects.filter(
            content_type=ContentType.objects.get_for_model(Book),
            object_id=book_id
        ).delete()

    @classmethod
    def remove_book_note_from_favorites(cls, book_note_id: int):
        Favorite.objects.filter(
            content_type=ContentType.objects.get_for_model(BookNote),
            object_id=book_note_id
        ).delete()


    @classmethod
    def add_book_to_favorites(cls, book_id: int, reason: str = '') -> Favorite:
        book = Book.objects.get(id=book_id)
        content_type = ContentType.objects.get_for_model(book)
        favorite, _ = Favorite.objects.get_or_create(
            content_type=content_type,
            object_id=book_id,
        )
        favorite.note = reason
        favorite.save()
        return favorite

    @classmethod
    def add_book_note_to_favorites(cls, note_id: int, reason: str = '') -> Favorite:
        note = BookNote.objects.get(id=note_id)
        content_type = ContentType.objects.get_for_model(note)
        favorite, _ = Favorite.objects.get_or_create(
            content_type=content_type,
            object_id=note_id,
        )
        favorite.note = reason
        favorite.save()
        return favorite
