import uuid
from django.db import models
from django.utils import timezone


class TelegramUser(models.Model):
    telegram_id = models.PositiveIntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4)
    date_created = models.DateTimeField(default=timezone.now)
