from .base import *


SECRET_KEY = os.environ.get('PERSONAL_SITE_SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = ("*",)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
