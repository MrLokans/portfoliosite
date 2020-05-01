import logging
from typing import Optional

import jwt
from django.conf import settings
from django.core.exceptions import PermissionDenied

from apps.internal_users.models import TelegramUser


logger = logging.getLogger()


class TelegramAuthMiddleware:

    TOKEN_HEADER_NAME = 'X-Auth-Telegram-Jwt'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = self.read_auth_token(request)
        if not jwt_token:
            # Not a telegram-based flow
            return self.get_response(request)
        request.telegram_user = self.user_from_token(jwt_token)
        return self.get_response(request)

    def user_from_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
            user_id = int(payload['user_id'])
            return TelegramUser.objects.get(telegram_id=user_id)
        except jwt.InvalidTokenError:
            logger.exception("User provided an invalid token")
            raise PermissionDenied
        except TelegramUser.DoesNotExist:
            logger.error(f"User provided the token for non-existent user (id={user_id})")
            raise PermissionDenied

    def read_auth_token(self, request) -> Optional[str]:
        return request.headers.get(self.TOKEN_HEADER_NAME)
