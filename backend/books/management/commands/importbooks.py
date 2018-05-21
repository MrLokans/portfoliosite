import logging

from tqdm import tqdm

from django.core.management.base import BaseCommand, CommandError

from books.models import Book

from dropbox import Dropbox
from dropbox.exceptions import DropboxException

from moonreader_tools.handlers import DropboxDownloader


logger = logging.getLogger(__name__)


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
                            default=200)

    def handle(self, *args, **kwargs):
        token = kwargs.get('token')
        if not token:
            raise CommandError("No dropbox token specified.")
        try:
            downloader = DropboxDownloader(Dropbox(token))
        except DropboxException as e:
            msg = "Incorrect dropbox token: {}"
            raise CommandError(msg.format(str(e)))

        books = downloader.get_books(book_count=kwargs['count'])
        book_dicts = [book.to_dict()
                      for book in tqdm(books, total=kwargs['count'])]

        Book.objects.load_new_entities(book_dicts)
