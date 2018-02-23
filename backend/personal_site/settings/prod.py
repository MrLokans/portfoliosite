from .base import *  # noqa

# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
# Take a look at this article

INSTALLED_APPS += [
        # Sentry error reporting
    'raven.contrib.django.raven_compat',
]

DEBUG = False
ALLOWED_HOSTS = ['.mrlokans.com', ]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


SENTRY_DSN = env('SENTRY_DSN')
RAVEN_CONFIG = {
    'dsn': SENTRY_DSN,
}
