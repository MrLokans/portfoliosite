import datetime
import logging
from typing import Iterable

from django.db import models

from personal_site.models_common import TimeTrackable
from apartments_analyzer.enums import BullettingStatusEnum


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ApartmentManager(models.Manager):

    def active(self):
        return (
            self.get_queryset()
            .filter(status=BullettingStatusEnum.ACTIVE.value)
        )

    def inactive(self):
        return (
            self.get_queryset()
            .filter(status=BullettingStatusEnum.INACTIVE.value)
        )

    def mark_active(self, urls: Iterable[str],
                    current_time: datetime.datetime=None) -> int:
        """
        Marks bulletings with given URLs
        as active
        """
        current_time = current_time or datetime.datetime.utcnow()
        qs = self.get_queryset()
        number_updated = (
            qs.filter(bullettin_url__in=urls)
            .update(status=BullettingStatusEnum.ACTIVE.value,
                    updated_at=current_time))
        return number_updated

    def mark_inactive(self, urls: Iterable[str],
                      current_time: datetime.datetime=None) -> int:
        """
        Marks bulletings with given URLs
        as active
        """
        current_time = current_time or datetime.datetime.utcnow()
        qs = self.get_queryset()
        number_updated = (
            qs.filter(bullettin_url__in=urls)
            .update(status=BullettingStatusEnum.INACTIVE.value,
                    updated_at=current_time))
        return number_updated


class Apartment(TimeTrackable):

    objects = ApartmentManager()

    address = models.TextField()
    price = models.IntegerField()

    description = models.TextField(default='')

    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    # Author profile URL
    author_url = models.URLField()
    # Original url of the apartment
    # TODO: find a way to deduplicate items (unique=True?)
    bullettin_url = models.URLField()

    status = models.SmallIntegerField(choices=[(x.value, x.name)
                                               for x in BullettingStatusEnum],
                                      default=BullettingStatusEnum.INACTIVE.value)

    def __str__(self):
        return ('Apartment(bullettin_url={}, price={})'
                .format(self.bullettin_url, self.price))


class ApartmentImage(models.Model):
    image_url = models.URLField()

    apartment = models.ForeignKey(Apartment,
                                  related_name='images',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return ('ApartmentImage(image_url={})'.format(self.image_url))


class ApartmentScrapingResults(models.Model):
    """
    This model is used to store scraping statistics
    after the crawler has been run.
    """
    time_started = models.DateTimeField()
    time_finished = models.DateTimeField(auto_now_add=True)
    succeeded = models.BooleanField()
    # If any errors
    error_message = models.TextField()
    total_errors = models.PositiveIntegerField()
    total_saved = models.PositiveIntegerField()
    total_active = models.PositiveIntegerField()
    total_inactive = models.PositiveIntegerField()
