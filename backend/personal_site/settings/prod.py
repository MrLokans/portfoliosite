from .base import *

import os

import raven

# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
# Take a look at this article

INSTALLED_APPS += [
        # Sentry error reporting
    'raven.contrib.django.raven_compat',
]

SECRET_KEY = 'ASDt32rqcajh12h523joh23#%!#%!#@%!Rasdd1r124135'
DEBUG = False
ALLOWED_HOSTS = ['.mrlokans.com', ]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


DSN = os.environ.get('PROD_SENTRY_DSN_KEY')
SENTRY_PROJECT = os.environ.get('PROD_SENTRY_PROJECT')
RAVEN_CONFIG = {
    'dsn': ('http://{dsn}@sentry_server:9000/sentry/{sentry_project}'
            .format(dsn=DSN, sentry_project=SENTRY_PROJECT)),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
    }
}
