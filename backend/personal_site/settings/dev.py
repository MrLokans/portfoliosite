import warnings
from .base import *  # noqa

import raven


DEBUG = True

ALLOWED_HOSTS = ("*",)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}
if os.environ.get('POSTGRES_DB'):
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
else:
    warnings.warn('Using SQLite database back-end '
                  'as no PostgreSQL settings are '
                  'present in the environment.')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    }

DSN = os.environ.get('DEV_SENTRY_DSN_KEY')
SENTRY_PROJECT = os.environ.get('DEV_SENTRY_PROJECT')
RAVEN_CONFIG = {
    # 'dsn': ('http://{dsn}@sentry_server:9000/{sentry_project}'
    #         .format(dsn=DSN, sentry_project=SENTRY_PROJECT)),
    'dsn': ('http://{dsn}@sentry_server:9000/3'
            .format(dsn=DSN, sentry_project=SENTRY_PROJECT)),
}
INSTALLED_APPS += ('rest_framework_swagger', )
