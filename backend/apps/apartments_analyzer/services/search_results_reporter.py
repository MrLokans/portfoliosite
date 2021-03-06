import datetime
import logging

import telegram
from django.db import transaction

from apps.apartments_analyzer.models import (
    UserSearch,
    ApartmentType,
    SoldApartments,
    RentApartment,
    SearchResults,
)


class TelegramReporter:
    """Responsible for generating and sending the report
    via telegram client.
    """

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
            ),
        )
        self.telegram_client.send_message(
            user_identifier,
            self.generate_reply(new_apartments=self.matched_apartments),
            parse_mode=telegram.ParseMode.HTML,
        )

    def generate_summary(self, search, new_apartments) -> str:
        return f"Найдено квартир по фильтру ({search.min_price}$ - {search.max_price}$) - {len(new_apartments)}"

    def generate_reply(self, new_apartments) -> str:
        return " \n".join(
            [
                f"<a href='{ap.bullettin_url}'>{ap.price_USD}$ - {ap.address}</a>"
                for ap in new_apartments
            ]
        )


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
            telegram_client=telegram.bot.Bot(
                token=django_settings.TELEGRAM_ACCESS_TOKEN
            )
        )

    def get_reporter(self, user_search, matched_apartments):
        return TelegramReporter(
            self.telegram_client,
            initial_search=user_search,
            matched_apartments=matched_apartments,
        )

    @classmethod
    def find_matching_apartments(cls, user_search: UserSearch, model=RentApartment):
        previously_parsed_urls = SearchResults.objects.all_matched_for_search(
            user_search
        )
        qs = (
            model.objects.active()
            .newer_than(datetime.timedelta(days=1))
            .in_price_range(user_search.min_price, user_search.max_price)
            .in_areas(user_search.get_search_polygons())
            .with_rooms_equal_or_more(user_search.min_rooms)
            .exclude_previous_search_results(previously_parsed_urls)
        )
        if not user_search.report_likely_agents:
            qs = qs.exclude(likely_agent=True)
        return qs

    def process_user_searches(self, *args, **kwargs):
        """For every persisted user search runs filters
        again newly loaded apartments and reports results
        if any."""
        searches = UserSearch.objects.prefetch_related("areas_of_interest").filter(
            is_active=True
        )
        for search in searches:
            self.log.info("Processing %s", search)
            model = self.__model_type_map__[search.apartment_type]
            matching_apartments = self.find_matching_apartments(search, model=model)
            failed = self.report_search_results(search, matching_apartments)
            if not failed:
                SearchResults.objects.create(
                    search_filter=search,
                    search_filter_version=search.search_version,
                    reported_urls=[ap.bullettin_url for ap in matching_apartments],
                )

    def report_search_results(self, search: UserSearch, matching_apartments) -> bool:
        """Send matching apartments to the user via available contact method."""
        has_failed = False
        for contact_details in search.available_contacts():
            reporter = self.get_reporter(search, matching_apartments)
            if reporter.should_report():
                try:
                    reporter.report(contact_details.contact_identifier)
                except telegram.error.BadRequest as e:
                    if getattr(e, 'message', '') == 'Chat not found':
                        self.remove_broken_user_search(search)
                        continue
                    self.__log_error(e, search)
                    has_failed = True
                except Exception as e:
                    self.__log_error(e, search)
                    has_failed = True
        return has_failed

    @transaction.atomic
    def remove_broken_user_search(self, search: UserSearch):
        self.log.info(f"Removing user search {search}")
        SearchResults.objects.filter(search_filter=search).delete()
        search.delete()

    def __log_error(self, exception: Exception, search: UserSearch):
        self.log.error(
            f"Error reporting search results (details={search})", exc_info=exception
        )
