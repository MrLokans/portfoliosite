from .base import *

# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
# Take a look at this article

SECRET_KEY = os.environ.get('PERSONAL_SITE_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
