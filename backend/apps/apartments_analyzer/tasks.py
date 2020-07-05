import logging
from typing import Optional

import dramatiq

from django.conf import settings

from apps.apartments_analyzer.models import UserSearch, UserSearchContact, ContactType
from apps.apartments_analyzer.services.search_results_reporter import SearchReporter

log = logging.getLogger(__name__)


@dramatiq.actor(max_retries=2)
def send_apartments_to_new_user(user_id: str):
    log.info("Sending apartments for the new user (id=%s).", user_id)
    print(UserSearch.objects.all().values())

    existing_contact: Optional[UserSearchContact] = UserSearchContact.objects.filter(
        contact_type=ContactType.TELEGRAM, contact_identifier=user_id
    ).first()
    if existing_contact is None:
        log.info("UserID (%s) does not have an associated contact yet, retrying.", user_id)
        # TODO: raise error
        raise Exception(f"No search for contact ({user_id})")
    existing_search = existing_contact.get_existing_search()
    if existing_search is None:
        log.info("UserID (%s) contact (%s) does not have an associated search yet, retrying.", user_id, existing_contact.pk)
        # TODO: raise error
        raise Exception(f"No search for contact ({existing_contact})")
    SearchReporter.from_settings(settings).process_user_search(existing_search, report_limit=10)
