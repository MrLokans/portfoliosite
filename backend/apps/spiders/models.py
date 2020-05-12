import enum

from django.contrib.postgres.fields import JSONField
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


@enum.unique
class SpiderEventKind(enum.IntEnum):
    SPIDER_STARTED = 0
    SPIDER_FINISHED = 1


class Spider(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    description = models.TextField(default="")
    associated_web_site = models.URLField()

    def __str__(self):
        return f"Spider - '{self.name}'"


class SpiderConfiguration(models.Model):
    associated_spider = models.ForeignKey(Spider, on_delete=models.CASCADE)
    website_part = models.CharField(max_length=255, blank=False, null=True, default="")
    search_words = ArrayField(models.CharField(max_length=64, blank=True))

    def __str__(self):
        return f"'{self.associated_spider.name}' - {self.website_part} - {len(self.search_words)}"


class SpiderEvent(models.Model):
    associated_spider = models.ForeignKey(Spider, on_delete=models.CASCADE)
    event_kind = models.PositiveSmallIntegerField(
        choices=[(tag.value, tag.name) for tag in SpiderEventKind]
    )
    event_data = JSONField()
    received_at = models.DateTimeField(auto_now=True)
