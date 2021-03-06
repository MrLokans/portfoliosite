import datetime
import decimal
import logging
import uuid
from typing import Iterable, Optional

from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models import F, UniqueConstraint

from apps.core.models_common import TimeTrackable
from .enums import BulletinStatusEnum
from .managers import SavedSearchManager
from .querysets import PrecalculatedStatsQuerySet, ApartmentsQueryset

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ApartmentType:
    SOLD = "S"
    RENT = "R"


class ContactType:
    EMAIL = "E"
    TELEGRAM = "T"


class ActiveInactiveManager(models.Manager):
    def get_queryset(self):
        return ApartmentsQueryset(model=self.model, using=self._db)

    def urls(self):
        return self.get_queryset().values_list("bullettin_url", flat=True)

    def mark_active(
        self, urls: Iterable[str], current_time: datetime.datetime = None
    ) -> int:
        """
        Marks bulletings with given URLs
        as active
        """
        current_time = current_time or datetime.datetime.utcnow()
        qs = self.get_queryset()
        number_updated = qs.filter(bullettin_url__in=urls).update(
            status=BulletinStatusEnum.ACTIVE.value,
            updated_at=current_time,
            last_active_parse_time=current_time,
        )
        return number_updated

    def mark_inactive(
        self, urls: Iterable[str], current_time: datetime.datetime = None
    ) -> int:
        """
        Marks bulletings with given URLs
        as active
        """
        current_time = current_time or datetime.datetime.utcnow()
        qs = self.get_queryset()
        number_updated = qs.filter(bullettin_url__in=urls).update(
            status=BulletinStatusEnum.INACTIVE.value, updated_at=current_time
        )
        return number_updated


class BaseApartmentBulletin(models.Model):
    EMPTY_BYN_PRICE = decimal.Decimal("0.0")
    DEFAULT_LAST_UPDATED_TEXT = "UNKNOWN"
    DEFAULT_USER_NAME = "UNKNOWN"

    class Meta:
        abstract = True

    # Original url of the apartment
    bullettin_url = models.URLField(unique=True)

    address = models.TextField()
    apartment_type = models.CharField(max_length=40)
    price_BYN = models.DecimalField(
        max_digits=10, decimal_places=2, default=EMPTY_BYN_PRICE
    )
    price_USD = models.IntegerField()

    description = models.TextField()

    location = gis_models.PointField(
        geography=False, srid=4326, default="POINT(0.0 0.0)"
    )

    # Author profile URL
    author_url = models.URLField()
    status = models.SmallIntegerField(
        choices=[(x.value, x.name) for x in BulletinStatusEnum],
        default=BulletinStatusEnum.INACTIVE.value,
    )

    user_phones = ArrayField(models.CharField(max_length=24), default=list)
    user_name = models.CharField(max_length=96, default=DEFAULT_USER_NAME)
    last_updated = models.CharField(max_length=24, default=DEFAULT_LAST_UPDATED_TEXT)

    last_active_parse_time = models.DateTimeField(null=True, blank=True)

    image_links = ArrayField(models.URLField(), default=list)

    subway_distances = JSONField(default=dict)

    likely_agent = models.BooleanField(null=True, blank=True)

    total_rooms = models.IntegerField(null=True)

    def __str__(self):
        return "Apartment(bullettin_url={}, price_USD={})".format(
            self.bullettin_url, self.price_USD
        )


class RentApartment(BaseApartmentBulletin, TimeTrackable):
    has_balcony = models.BooleanField()
    has_conditioner = models.BooleanField()
    has_fridge = models.BooleanField()
    has_furniture = models.BooleanField()
    has_internet = models.BooleanField()
    has_kitchen_furniture = models.BooleanField()
    has_oven = models.BooleanField()
    has_tv = models.BooleanField()
    has_washing_machine = models.BooleanField()

    objects = ActiveInactiveManager.from_queryset(ApartmentsQueryset)()


class SoldApartments(BaseApartmentBulletin, TimeTrackable):

    on_floor = models.IntegerField()
    total_floors = models.IntegerField()

    total_area = models.FloatField()
    living_area = models.FloatField()
    kitchen_area = models.FloatField()

    house_type = models.TextField()
    balcony_details = models.TextField()
    parking_details = models.TextField()
    ceiling_details = models.TextField(default="")

    objects = ActiveInactiveManager.from_queryset(ApartmentsQueryset)()


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
    invalid_urls = ArrayField(models.URLField(), default=list)

    new_items = models.PositiveIntegerField(default=0)
    updated_items = models.PositiveIntegerField(default=0)

    @property
    def time_taken(self):
        return self.time_finished - self.time_started

    def __repr__(self):
        return "ApartmentScrapingResults(" "time_finished={0}, succeeded={1})".format(
            self.time_finished, self.succeeded
        )

    __str__ = __repr__


class AreaOfInterest(gis_models.Model):
    """Apartments in active search areas are sent to user."""

    name = models.CharField(max_length=50)
    poly = gis_models.PolygonField(geography=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Areas of interest"

    def __str__(self):
        return self.name


class UserSearchContact(TimeTrackable):

    MAX_DESCRIPTION_LENGTH: int = 120
    CONTACT_TYPE_CHOICES = (
        (ContactType.EMAIL, "Email"),
        (ContactType.TELEGRAM, "Telegram messenger"),
    )
    contact_type = models.CharField(max_length=1, choices=CONTACT_TYPE_CHOICES)
    contact_identifier = models.CharField(max_length=120)
    description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH, default="")

    class Meta:
        verbose_name_plural = "User contacts"
        constraints = (
            UniqueConstraint(
                fields=("contact_type", "contact_identifier"), name="unique_contact"
            ),
        )

    def get_existing_search(self) -> Optional["UserSearch"]:
        return self.usersearch_set.first()

    def __str__(self):
        return f"UserContact(type={self.contact_type}, id={self.contact_identifier}, description={self.description})"


class UserSearch(TimeTrackable):

    APARTMENT_TYPE_CHOICES = (
        (ApartmentType.SOLD, "На продажу"),
        (ApartmentType.RENT, "В аренду"),
    )
    DEFAULT_SEARCH_VERSION = 0

    min_price = models.PositiveIntegerField(default=0, help_text="Минимальная цена в $")
    max_price = models.PositiveIntegerField(
        default=300, help_text="Максимальная цена в $"
    )
    min_rooms = models.PositiveSmallIntegerField(
        default=0, help_text="Минимальное количество комнат"
    )
    is_active = models.BooleanField(default=True)

    contacts = models.ManyToManyField(UserSearchContact)
    areas_of_interest = models.ManyToManyField(AreaOfInterest)

    apartment_type = models.CharField(max_length=1, choices=APARTMENT_TYPE_CHOICES)

    report_likely_agents = models.BooleanField(default=True)

    search_version = models.PositiveIntegerField(
        default=DEFAULT_SEARCH_VERSION, help_text="Number of search modifications"
    )

    class Meta:
        verbose_name_plural = "Persisted user searches"

    def as_displayed_to_user(self) -> str:
        buffer = []
        buffer.append(f"Поиск активен: {self.is_active and 'Да' or 'Нет'}")
        buffer.append(f"Тип поиска: {self.display_search_type}")
        buffer.append(f"Диапазон цен: {self.min_price} - {self.max_price}$")
        buffer.append(f"Количество комнат: {self.min_rooms}+")
        return "\n".join(buffer)

    @property
    def display_search_type(self):
        return dict(self.APARTMENT_TYPE_CHOICES)[self.apartment_type]

    def increase_version(self):
        self.search_version = F("search_version") + 1

    def get_search_polygons(self):
        return [a.poly for a in self.areas_of_interest.all()]

    def available_contacts(self):
        return self.contacts.filter(contact_type=ContactType.TELEGRAM)

    @property
    def main_contact(self):
        return self.contacts.first()

    def __str__(self):
        contact = self.main_contact
        if not contact:
            return "Search by unknown contact"
        identity = contact.description or contact.contact_identifier
        return f"Search by {identity} ({self.min_price}$ - {self.max_price}$)"


class SearchResults(TimeTrackable):

    search_filter = models.ForeignKey(UserSearch, on_delete=models.DO_NOTHING)
    search_filter_version = models.PositiveIntegerField(
        default=UserSearch.DEFAULT_SEARCH_VERSION
    )
    reported_urls = ArrayField(models.CharField(max_length=255), default=list)

    objects = SavedSearchManager()

    class Meta:
        verbose_name_plural = "Reported search results"

    def __str__(self):
        return f"{self.created_at} - {len(self.reported_urls)} urls"


class CityRegion(TimeTrackable):
    region_name = models.CharField(
        max_length=120, unique=True, db_index=True, primary_key=True
    )
    polygon = gis_models.MultiPolygonField(geography=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)

    class Meta:
        verbose_name_plural = "City Regions"

    def __str__(self):
        return f"{self.region_name}"


class PrecalculatedApartmentStats(TimeTrackable):
    statistics = JSONField()

    objects = PrecalculatedStatsQuerySet.as_manager()
