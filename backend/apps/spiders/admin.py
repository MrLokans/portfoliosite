from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django_json_widget.widgets import JSONEditorWidget

from apps.spiders import models


class SpiderConfigurationInline(admin.TabularInline):
    model = models.SpiderConfiguration


@admin.register(models.Spider)
class SpidersAdmin(admin.ModelAdmin):
    inlines = [SpiderConfigurationInline]


@admin.register(models.SpiderConfiguration)
class SpidersConfigurationAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


@admin.register(models.SpiderEvent)
class SpidersEventAdmin(admin.ModelAdmin):
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
