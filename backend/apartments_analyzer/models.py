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
                    current_time: datetime.datetime=None):
        """
        Marks bulletings with given URLs
        as active
        """
        current_time = current_time or datetime.datetime.utcnow()
        qs = self.get_queryset()
        (qs.filter(bullettin_url__in=urls)
         .update(status=BullettingStatusEnum.ACTIVE.value,
                 updated_at=current_time))

    def mark_inactive(self, urls: Iterable[str],
                      current_time: datetime.datetime=None):
        """
        Marks bulletings with given URLs
        as active
        """
        current_time = current_time or datetime.datetime.utcnow()
        qs = self.get_queryset()
        (qs.filter(bullettin_url__in=urls)
         .update(status=BullettingStatusEnum.INACTIVE.value,
                 updated_at=current_time))


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