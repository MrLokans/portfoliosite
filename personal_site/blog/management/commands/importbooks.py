from django.core.management.base import BaseCommand, CommandError

from books.models import Book, BookNote

from dropbox.rest import ErrorResponse

from moonreader_tools.handlers import DropboxDownloader


class Command(BaseCommand):
    help = """Import books notes and reading statistics from
    Dropbox and dumps them to database"""

    def add_arguments(self, parser):
        parser.add_argument('--token',
                            type=str,
                            help='Dropbox access token')
        parser.add_argument('--count',
                            type=int,
                            help='Number of books to download',
                            default=20)

    def handle(self, *args, **kwargs):
        token = kwargs.get('token')
        if not token:
            raise CommandError("No dropbox token specified.")
        try:
            downloader = DropboxDownloader(token)
        except ErrorResponse as e:
            msg = "Incorrect dropbox token: {}"
            raise CommandError(msg.format(str(e)))

        books = downloader.get_books(book_count=kwargs['count'])

        book_dicts = [book.to_dict() for book in books]

        # We delete all objects here
        # Absolutely, worst idea ever
        # TODO:
        BookNote.objects.all().delete()
        Book.objects.all().delete()

        for book_dict in book_dicts:
            Book.from_dict(book_dict)
