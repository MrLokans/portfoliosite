from django.db import models

from personal_site.models_common import TimeTrackable


class FavoriteLink(TimeTrackable):
    """
    This model is used to store link to any
    interesting resource on the internet
    """
    name = models.CharField(max_length=120, blank=True)
    url = models.URLField(max_length=320, unique=True)
    comment = models.TextField(blank=True)

    def __repr__(self):
        return 'FavoriteLink(url={})'.format(self.url)
