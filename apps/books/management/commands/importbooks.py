import json
import logging
import os
from typing import List, Dict


from django.core.management.base import CommandError
from django.conf import settings

from tqdm import tqdm
from dropbox import Dropbox
from dropbox.exceptions import DropboxException

from moonreader_tools.handlers import DropboxDownloader

from apps.books.models import Book
from personal_site.base_command import BaseSingletonCommand

logger = logging.getLogger(__name__)


class Command(BaseSingletonCommand):
    help = """Import books notes and reading statistics from
    Dropbox and dump them to database"""

    def add_arguments(self, parser):
        parser.add_argument("--token", type=str, help="Dropbox access token")
        parser.add_argument(
            "--count", type=int, help="Number of books to download", default=1000
        )
        parser.add_argument(
            "--file",
            type=str,
            help="JSON file, containing parsed books",
            required=False,
        )

    def handle(self, *args, **kwargs):
        token = self._read_access_token(kwargs)
        if kwargs.get("file"):
            books = self.get_books_from_file(kwargs.get("file"))
        elif token:
            books = self.download_books(token, kwargs["count"])
        else:
            raise CommandError("Either dropbox token or books file should be provided")
        Book.objects.load_new_entities(books)

    def download_books(self, token, book_count: int) -> List[Dict]:
        try:
            downloader = DropboxDownloader(Dropbox(token))
        except DropboxException as e:
            msg = "Incorrect dropbox token: {}"
            raise CommandError(msg.format(str(e)))
        books = downloader.get_books(book_count=book_count)
        return [book.to_dict() for book in tqdm(books, total=book_count)]

    def get_books_from_file(self, books_file: str) -> List[Dict]:
        assert os.path.isfile(
            books_file
        ), "Provided file is not a file or does not exist."
        with open(books_file, "r") as f:
            json_data = json.load(f)
            assert isinstance(json_data, list)
            return json_data

    def _read_access_token(self, command_kwargs: Dict) -> str or None:
        return command_kwargs.get("token") or settings.DROPBOX_ACCESS_TOKEN
