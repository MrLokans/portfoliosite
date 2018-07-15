import logging
from collections import defaultdict
from typing import Dict, List

from django.db import transaction


logger = logging.getLogger(__name__)


class Deduplicator(object):

    def __init__(self, apartment_cls, field_to_track: str):
        self.apartment_cls = apartment_cls
        self.field_to_track = field_to_track

    def remove_duplicate_apartments(self):
        """
        We pass apartment model class as it is required
        to be correctly run in migrations (model fields may differ)
        """
        entries_duplicates = self._get_url_count()
        entries_to_remove = self._get_entries_to_remove(entries_duplicates)
        self._delete_duplicated_entries_from_db(entries_to_remove)

    def _get_url_count(self) -> Dict[str, List]:
        logger.info('Finding duplicate entries.')
        entries = self.apartment_cls.objects\
            .values_list('id', self.field_to_track, 'updated_at')
        entries_duplicates = defaultdict(list)
        for entry in entries:
            url = entry[1]
            entries_duplicates[url].append(entry)
        return entries_duplicates

    def _get_entries_to_remove(self,
                               url_dict: Dict[str, List]) -> List:
        logger.info('Finding items to remove.')
        entries_to_remove = []
        for _, entry_list in url_dict.items():
            if len(entry_list) < 2:
                continue
            # We exclude the latest entry marking
            # other ones as deleted
            entry_list.remove(max(entry_list, key=lambda x: x[2]))
            entries_to_remove.extend(entry_list)
        return entries_to_remove

    def _delete_duplicated_entries_from_db(self,
                                           entries_to_remove: List[tuple]):
        logger.info('Deleting items.')
        _ids_to_remove = [e[0] for e in entries_to_remove]
        with transaction.atomic():
            deleted_qs = self.apartment_cls.objects\
                .filter(id__in=_ids_to_remove)
            deleted_qs.delete()
