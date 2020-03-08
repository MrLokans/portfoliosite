from django.apps import AppConfig


class ApartmentsConfig(AppConfig):
    name = "apps.apartments_analyzer"

    def ready(self):
        from apps.apartments_analyzer import signals
