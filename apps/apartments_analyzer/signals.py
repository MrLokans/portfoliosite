from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.apartments_analyzer.models import UserSearch


@receiver(pre_save, sender=UserSearch)
def update_search_version(sender, instance: UserSearch, **kwargs):
    instance.increase_version()
