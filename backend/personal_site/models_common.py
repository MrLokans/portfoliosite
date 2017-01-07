from django.db import models


class TimeTrackable(models.Model):
    """
    Abstract base class model used to add
    created_at and updated_at fields to multiple models
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
