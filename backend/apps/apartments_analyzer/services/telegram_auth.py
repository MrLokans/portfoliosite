import hashlib
import hmac
from datetime import datetime

from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from apps.apartments_analyzer import entities
from apps.apartments_analyzer.models import UserSearchContact, ContactType, UserSearch
from apps.internal_users.models import TelegramUser


class TelegramUserService:

    REQUIRED_FIELDS = (
        'id',
        'hash',
        'username',
        'auth_date',
    )

    def __init__(self, telegram_token):
        self.__telegram_token = telegram_token

    @classmethod
    def from_settings(cls, django_settings):
        return cls(
            telegram_token=django_settings.TELEGRAM_ACCESS_TOKEN
        )

    def validate_payload(self, telegram_payload: dict):
        for field in self.REQUIRED_FIELDS:
            if field not in telegram_payload:
                raise ValidationError(detail=f"Field '{field}' is missing in the request")

    def verify_telegram_payload(self, telegram_payload):
        self.validate_payload(telegram_payload)
        query_hash = telegram_payload.pop('hash')
        secret = hashlib.sha256(self.__telegram_token.encode('utf-8')).digest()
        check_string = '\n'.join(
            f"{key}={value}"
            for (key, value) in sorted(telegram_payload.items())
        )
        check_hash = hmac.new(
            secret,
            check_string.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        if datetime.now().timestamp() - int(telegram_payload['auth_date']) > 86400:
            raise ValidationError(
                detail="Telegram auth data is outdated.",
                code="invalid_telegram_credentials"
            )
        if query_hash != check_hash:
            raise ValidationError(
                detail="Invalid telegram data",
                code="invalid_telegram_credentials"
            )

    @transaction.atomic
    def get_or_create_internal_user(
        self, user_data: entities.TelegramUserData
    ) -> TelegramUser:
        username = user_data.possible_username()
        internal_user, _ = TelegramUser.objects.get_or_create(
            telegram_id=user_data.id,
            defaults={'username': username}
        )
        internal_user.username = username
        internal_user.save(update_fields=("username", ))
        contact, _ = UserSearchContact.objects.get_or_create(
            contact_type=ContactType.TELEGRAM,
            contact_identifier=str(user_data.id),
            defaults={"description": username}
        )
        contact.description = username
        contact.save(update_fields=("description", ))
        return internal_user

    def get_search(self, user: TelegramUser) -> UserSearch:
        query = Q(contacts__contact_identifier= user.pk)
        query &= Q(contacts__contact_type=ContactType.TELEGRAM)
        qs = UserSearch.objects.filter(query)
        assert qs.count() == 1, "There should exactly be one search for the user"
        return qs.first()
