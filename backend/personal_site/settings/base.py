# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import environ

env = environ.Env(
        DEBUG=(bool, False),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ALLOWED_HOSTS = []

APPEND_SLASH = True


INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'django_extensions',
    'admin_honeypot',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'import_export',
    'pagedown',
    'rest_framework',
    # Sentry error reporting
    'raven.contrib.django.raven_compat',

    # Custom apps
    'about_me',
    'apartments_analyzer',
    'blog',
    'books',
    'contributions',
    'statistics',
    'personal_site',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'personal_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },

    },
]

WSGI_APPLICATION = 'personal_site.wsgi.application'

DATABASES = {
    'default': env.db()
}
SECRET_KEY = env('DJANGO_SECRET_KEY')

if os.environ.get('REDIS_URL'):
    CACHES = {
        'default': env.cache('REDIS_URL'),
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     os.environ.get('DJANGO_STATIC_DIR', os.path.join(BASE_DIR, 'staticfiles')),
# ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# print(os.path.exists(STATICFILES_DIRS[0]))
# print(STATICFILES_DIRS)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

LOGIN_REDIRECT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'personal_site.paginators.CustomPagination',
    'PAGE_SIZE': 25,
}

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

SITE_ID = 1

# sentry configuration
SENTRY_DSN = env('SENTRY_DSN', default='')
if SENTRY_DSN:
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }
