from typing import Set

from django.db import models


class SavedSearchManager(models.Manager):


    def all_matched_for_search(self, for_search) -> Set[str]:
        matched_urls = set()
        matched_filters = self.model.objects.filter(
            search_filter=for_search,
            search_filter_version=for_search.search_version
        ).values('reported_urls')
        for filter in matched_filters:
            matched_urls.update(filter['reported_urls'])
        return matched_urls
