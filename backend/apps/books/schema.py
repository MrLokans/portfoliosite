import graphene

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from apps.books.models import Book, BookNote


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        filter_fields = {"original_title": ["icontains"]}
        interfaces = (graphene.relay.Node,)

    proper_title = graphene.String()


class BookNoteType(DjangoObjectType):
    class Meta:
        model = BookNote
        filter_fields = {"text": ["icontains"]}
        interfaces = (graphene.relay.Node,)


class Query:
    all_books = DjangoFilterConnectionField(BookType)
    all_notes = DjangoFilterConnectionField(BookNoteType)

    random_note = graphene.Field(BookNoteType)

    def resolve_random_note(self, _, **kwargs):
        return BookNote.objects.random_note()

    def resolve_all_books(self, _, **kwargs):
        return Book.objects.non_empty().prefetch_related("notes")

    def resolve_all_notes(self, _, **kwargs):
        return BookNote.objects.prefetch_related("book")
