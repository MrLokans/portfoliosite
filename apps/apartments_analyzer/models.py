import datetime
import decimal
import logging
from typing import Iterable

from django.db import models
from django.contrib.postgres.fields import ArrayField

from personal_site.models_common import TimeTrackable
from .enums import BullettingStatusEnum


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
                    current_time: datetime.datetime = None) -> int:
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
                      current_time: datetime.datetime = None) -> int:
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

    _EMPTY_BYN_PRICE = decimal.Decimal('0.0')
    _DEFAULT_LAST_UPDATED_TEXT = 'UNKNOWN'
    _DEFAULT_USER_NAME = 'UNKNOWN'

    # Original url of the apartment
    bullettin_url = models.URLField(unique=True)

    address = models.TextField()
    apartment_type = models.CharField(max_length=40)
    price_BYN = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=_EMPTY_BYN_PRICE,
    )
    price_USD = models.IntegerField()

    description = models.TextField()

    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    # Author profile URL
    author_url = models.URLField()
    status = models.SmallIntegerField(choices=[(x.value, x.name)
                                               for x in BullettingStatusEnum],
                                      default=BullettingStatusEnum.INACTIVE.value)

    user_phones = ArrayField(models.CharField(max_length=24), default=[])
    user_name = models.CharField(max_length=96, default=_DEFAULT_USER_NAME)
    last_updated = models.CharField(max_length=24, default=_DEFAULT_LAST_UPDATED_TEXT)

    image_links = ArrayField(models.URLField(), default=[])

    has_balcony = models.BooleanField()
    has_conditioner = models.BooleanField()
    has_fridge = models.BooleanField()
    has_furniture = models.BooleanField()
    has_internet = models.BooleanField()
    has_kitchen_furniture = models.BooleanField()
    has_oven = models.BooleanField()
    has_tv = models.BooleanField()
    has_washing_machine = models.BooleanField()

    objects = ApartmentManager()

    def __str__(self):
        return ('Apartment(bullettin_url={}, price_USD={})'
                .format(self.bullettin_url, self.price_USD))


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
    # Number of newly added apartments
    total_active = models.PositiveIntegerField()
    total_inactive = models.PositiveIntegerField()
    # URLs we were unable to process
    invalid_urls = ArrayField(models.URLField(), default=[])

    new_items = models.PositiveIntegerField(default=0)
    updated_items = models.PositiveIntegerField(default=0)

    @property
    def time_taken(self):
        return self.time_finished - self.time_started

    def __repr__(self):
        return ('ApartmentScrapingResults('
                'time_finished={0}, succeeded={1})'
                .format(self.time_finished, self.succeeded))

    __str__ = __repr__
