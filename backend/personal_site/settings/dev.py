from .base import *

import raven


SECRET_KEY = 'test'
DEBUG = True

ALLOWED_HOSTS = ("*",)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}

DSN = os.environ.get('DEV_SENTRY_DSN_KEY')
SENTRY_PROJECT = os.environ.get('DEV_SENTRY_PROJECT')
RAVEN_CONFIG = {
    'dsn': ('http://{dsn}@sentry_server:19000/{sentry_project}'
            .format(dsn=DSN, sentry_project=SENTRY_PROJECT)),
}

INSTALLED_APPS += ('rest_framework_swagger', )
