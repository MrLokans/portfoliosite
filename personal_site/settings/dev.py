from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ("*",)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler"}},
}
