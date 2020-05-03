# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import environ

env = environ.Env(DEBUG=(bool, False), TELEGRAM_ACCESS_TOKEN=(str, ""),)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ALLOWED_HOSTS = []

APPEND_SLASH = True

PREREQUSITE_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    # Third party
    "django_extensions",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "import_export",
    "pagedown",
    "rest_framework",
    "rest_framework_gis",
    "corsheaders",
    "generic_relations",
    "django_json_widget",
    "django_better_admin_arrayfield.apps.DjangoBetterAdminArrayfieldConfig",
    "graphene_django",
]

WAGTAIL_APPS = [
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "taggit",
]

PROJECT_APPS = [
    "apps.core",
    "apps.about_me",
    "apps.apartments_analyzer.apps.ApartmentsConfig",
    "apps.blog",
    "apps.books",
    "apps.spiders",
    "apps.internal_users",
]


INSTALLED_APPS = PREREQUSITE_APPS + WAGTAIL_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.internal_users.middlewares.TelegramAuthMiddleware",
]


ROOT_URLCONF = "apps.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]

WSGI_APPLICATION = "apps.core.wsgi.application"

DATABASES = {"default": env.db()}

SECRET_KEY = env("DJANGO_SECRET_KEY")


REDIS_URL = os.environ.get("REDIS_URL", "")

if REDIS_URL:
    CACHES = {"default": env.cache("REDIS_URL")}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Minsk"
USE_I18N = True
USE_L10N = True
USE_TZ = True


gettext = lambda s: s
LANGUAGES = (("ru", gettext("Russian")), ("en", gettext("English")))


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGIN_REDIRECT_URL = "/"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "apps.core.paginators.CustomPagination",
    "PAGE_SIZE": 25,
}


SITE_ID = 1

DROPBOX_ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS_TOKEN")


CORS_ORIGIN_WHITELIST = ("http://localhost:8100", "http://127.0.0.1:8000")


WAGTAIL_SITE_NAME = "mrlokans.com"

GRAPHENE = {
    "SCHEMA": "core.schema.schema",
}

TELEGRAM_ACCESS_TOKEN = env.str("TELEGRAM_BOT_ACCESS_TOKEN")
TELEGRAM_ADMIN_CHAT_ID = env.str("TELEGRAM_ADMIN_CHAT_ID")

GDAL_LIBRARY_PATH = env.str("GDAL_LIBRARY_PATH", default="")
GEOS_LIBRARY_PATH = env.str("GEOS_LIBRARY_PATH", default="")

SENTRY_DSN = env.str("SENTRY_DSN", default="")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )
