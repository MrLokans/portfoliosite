from .base import *  # noqa

# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
# Take a look at this article

DEBUG = False
ALLOWED_HOSTS = ['.mrlokans.com', ]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)
