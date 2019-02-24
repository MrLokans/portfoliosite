from .base import *  # noqa

# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
# Take a look at this article

DEBUG = False
ALLOWED_HOSTS = (
    '.mrlokans.com',
    # Health checks
    'http://localhost:8000'
)

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
