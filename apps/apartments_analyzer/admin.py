import warnings

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.apartments_analyzer.filters import RentedPriceRangeFilter, RoomCountFilter, SoldPriceRangeFilter
from .models import (
    RentApartment,
    ApartmentScrapingResults,
    SoldApartments)


class ApartmentsResource(resources.ModelResource):
    # pylint: disable=no-init
    class Meta:
        model = RentApartment


IMAGE_TEMPLATE = """
<a href='{0}' target='blank_'>
    <img style='width: 300px; padding-top: 5px;' src='{0}'>
</a>
"""


class BaseApartmentAdmin(admin.ModelAdmin):

    class Media:
        key_set = hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY
        if not key_set:
            warnings.warn('GOOGLE_MAPS_API_KEY setting is not set. '
                          'Google Map will not be displayed in the admin site.')
        else:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )

    readonly_fields = ('bulletin_images',)
    list_display = ('bullettin_url', 'address', 'price_USD', 'price_BYN',
                    'latitude', 'longitude', 'status',
                    'created_at', 'updated_at', 'images_count')
    search_fields = ('address', 'price_USD')

    def bulletin_images(self, obj):
        return format_html_join(
            mark_safe('<br/>'),
            IMAGE_TEMPLATE,
            ((link, ) for link in obj.image_links)
        )

    def images_count(self, obj):
        return len(obj.image_links)

    images_count.admin_order_field = 'images_count'


class ApartmentAdmin(BaseApartmentAdmin, ImportExportModelAdmin):

    list_filter = [RentedPriceRangeFilter, RoomCountFilter]

    resource_class = ApartmentsResource


class SoldApartmentAdmin(BaseApartmentAdmin, ImportExportModelAdmin):

    list_filter = [SoldPriceRangeFilter, ]


class ApartmentScrapeStatsAdmin(admin.ModelAdmin):
    fields = ('time_started',
              'time_finished',
              'succeeded',
              'error_message',
              'total_errors',
              'total_saved',
              'total_active',
              'total_inactive',
              'time_taken',
              'invalid_urls',
              'new_items',
              'updated_items',
              )
    readonly_fields = fields
    list_display = ('time_started', 'time_finished', 'succeeded',
                    'total_saved', 'total_errors',
                    'time_taken')


admin.site.register(RentApartment, ApartmentAdmin)
admin.site.register(SoldApartments, SoldApartmentAdmin)
admin.site.register(ApartmentScrapingResults, ApartmentScrapeStatsAdmin)
