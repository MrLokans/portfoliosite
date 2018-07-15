import logging
import os

from django.core.files import locks
from django.core.management import BaseCommand


LOG = logging.getLogger(__name__)


class BaseSingletonCommand(BaseCommand):
    """
    Command, that may only be run sequentially (once at a time).

    Uses file-based django locks as a synchronization primitive.

    Override .get_lock_path() method to return lock file path
    """

    def get_lock_path(self):
        class_name = repr(self.__class__).replace("<class '", "").replace("'>", "")
        lock_path = os.path.join('/tmp', class_name + '.lock')
        LOG.debug("Command log path: %s", lock_path)
        return lock_path

    def execute(self, *args, **kwargs):
        lock_path = self.get_lock_path()
        with open(lock_path, 'wb') as lock_file:
            try:
                locks.lock(lock_file, locks.LOCK_EX)
                return super().execute(*args, **kwargs)
            finally:
                try:
                    os.unlink(lock_path)
                except Exception:
                    LOG.exception("Error removing file lock %s", lock_path)
