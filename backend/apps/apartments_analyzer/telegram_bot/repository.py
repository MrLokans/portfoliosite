from typing import Tuple

from django.db import transaction

from apps.apartments_analyzer.models import UserSearch, ContactType, ApartmentType, UserSearchContact, AreaOfInterest


class TelegramSearchRepository:

    DEFAULT_SEARCH_REGION = "Минск"

    def __qs_for_contact_id(self, contact_id: str):
        return UserSearch.objects.filter(
            contacts__contact_type=ContactType.TELEGRAM,
            contacts__contact_identifier=contact_id,
        )

    @transaction.atomic
    def get_or_create_for_user(self, contact_id: str, search_type=ApartmentType.RENT) -> Tuple[bool, UserSearch]:
        existing_conversation, created = UserSearchContact.objects.get_or_create(
            contact_type=ContactType.TELEGRAM, contact_identifier=contact_id
        )
        existing_search = existing_conversation.get_existing_search()
        if not existing_search:
            existing_search = UserSearch(apartment_type=search_type)
            existing_search.save()
            self._add_default_search_region(existing_search)
            existing_search.contacts.add(existing_conversation)
        return created, existing_search

    @transaction.atomic
    def update_search_price_range(
        self, contact_id: str, min_price: int, max_price: int
    ):
        self.__qs_for_contact_id(contact_id).update(
            min_price=min_price, max_price=max_price,
        )

    @transaction.atomic
    def update_min_room_count(self, contact_id: str, min_room_count: int):
        assert min_room_count >= 0
        self.__qs_for_contact_id(contact_id).update(min_rooms=min_room_count,)

    @transaction.atomic
    def set_contact_description(self, contact_id, description: str):
        UserSearchContact.objects.filter(contact_identifier=contact_id).update(description=description)

    @transaction.atomic
    def enable_for_user(self, contact_id: str):
        self.__qs_for_contact_id(contact_id).update(is_active=True)

    @transaction.atomic
    def disable_for_user(self, contact_id: str):
        self.__qs_for_contact_id(contact_id).update(is_active=False)

    def _add_default_search_region(self, user_search: UserSearch):
        default_region = AreaOfInterest.objects.filter(name=self.DEFAULT_SEARCH_REGION).first()
        if default_region is not None:
            user_search.areas_of_interest.add(default_region)