from .base import *

import os

import raven

# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
# Take a look at this article

SECRET_KEY = 'ASDt32rqcajh12h523joh23#%!#%!#@%!Rasdd1r124135'
DEBUG = False
ALLOWED_HOSTS = ['.mrlokans.com', ]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


DSN = os.environ.get('PROD_SENTRY_DSN_KEY')
SENTRY_PROJECT = os.environ.get('PROD_SENTRY_PROJECT')
RAVEN_CONFIG = {
    'dsn': ('http://{dsn}@sentry_server:19000/{sentry_project}'
            .format(dsn=DSN, sentry_project=SENTRY_PROJECT)),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
