from .base import *

# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
# Take a look at this article

SECRET_KEY = os.environ.get('PERSONAL_SITE_SECRET_KEY', 'none')
DEBUG = False
ALLOWED_HOSTS = ('*', )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PERSONAL_SITE_DB_NAME'),
        'USER': os.environ.get('PERSONAL_SITE_DB_USER'),
        'PASSWORD': os.environ.get('PERSONAL_SITE_DB_PASSWORD'),
        'HOST': os.environ.get('PERSONAL_SITE_DB_HOST', 'localhost'),
        'PORT': os.environ.get('PERSONAL_SITE_DB_PORT'),
    }
}
