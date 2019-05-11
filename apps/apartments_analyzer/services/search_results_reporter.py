import datetime
import logging
from typing import List

import telegram

from apps.apartments_analyzer.models import UserSearch, ApartmentType, SoldApartments, RentApartment, ContactType, \
    SearchResults


class TelegramReporter:

    def __init__(self, telegram_client, initial_search: UserSearch, matched_apartments):
        self.telegram_client = telegram_client
        self.initial_search = initial_search
        self.matched_apartments = matched_apartments

    def should_report(self) -> bool:
        return bool(len(self.matched_apartments))

    def report(self, user_identifier):
        self.telegram_client.send_message(
            user_identifier,
            self.generate_summary(
                self.initial_search, new_apartments=self.matched_apartments
            )
        )
        self.telegram_client.send_message(
            user_identifier,
            self.generate_reply(new_apartments=self.matched_apartments),
            parse_mode=telegram.ParseMode.HTML
        )

    def generate_summary(self, search, new_apartments) -> str:
        return f"Найдено квартир по фильтру ({search.min_price}$ - {search.max_price}$) - {len(new_apartments)}"

    def generate_reply(self, new_apartments) -> str:
        return " \n".join([
            f"<a href='{ap.bullettin_url}'>{ap.price_USD}$ - {ap.address}</a>"
            for ap in new_apartments
        ])


class SearchReporter:

    __model_type_map__ = {
        ApartmentType.SOLD: SoldApartments,
        ApartmentType.RENT: RentApartment,
    }

    def __init__(self, telegram_client):
        self.log = logging.getLogger(self.__class__.__name__)
        self.telegram_client = telegram_client

    @classmethod
    def from_settings(cls, django_settings):
        return cls(
            telegram_client=telegram.bot.Bot(token=django_settings.TELEGRAM_ACCESS_TOKEN)
        )

    def process_user_searches(self, *args, **kwargs):
        searches = UserSearch.objects.prefetch_related("areas_of_interest")
        for search in searches:
            self.log.info(f"Processing {search}")
            model = self.__model_type_map__[search.apartment_type]
            previously_parsed_urls = self.previously_parsed_urls(search)
            matching_apartments = (
                model.objects
                    .active()
                    .newer_than(datetime.timedelta(days=1))
                    .in_price_range(search.min_price, search.max_price)
                    .in_areas(search.get_search_polygons())
                    .exclude(bullettin_url__in=previously_parsed_urls)
            )
            self.report_search_results(search, matching_apartments)
            SearchResults.objects.create(
                search_filter=search,
                reported_urls=[ap.bullettin_url for ap in matching_apartments]
            )

    def previously_parsed_urls(self, search: UserSearch) -> List[str]:
        last_search = SearchResults.objects.filter(search_filter=search).order_by('created_at').last()
        return last_search.reported_urls if last_search else []

    def report_search_results(self, search: UserSearch, matching_apartments):
        # TODO: add flexible client types
        for contact_details in search.contacts.all():
            if contact_details.contact_type != ContactType.TELEGRAM:
                self.log.warning("Currently telegram is supported only.")
            reporter = TelegramReporter(
                self.telegram_client, initial_search=search, matched_apartments=matching_apartments
            )
            reporter.should_report() and reporter.report(contact_details.contact_identifier)
