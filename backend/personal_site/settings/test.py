from .base import *


SECRET_KEY = 'test'
DEBUG = True

ALLOWED_HOSTS = ("*",)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
