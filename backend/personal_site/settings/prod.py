from .base import *

# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
# Take a look at this article

SECRET_KEY = os.environ.get('PERSONAL_SITE_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['.mrlokans.com', ]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
