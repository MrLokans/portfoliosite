from .base import *


SECRET_KEY = os.environ.get('PERSONAL_SITE_SECRET_KEY')
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
