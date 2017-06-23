import warnings

from django.conf import settings
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from apartments_analyzer.models import (
    Apartment,
    ApartmentImage,
    ApartmentScrapingResults
)


IMAGE_TEMPLATE = """
<a href='{0}' target='blank_'>
    <img style='width: 300px; padding-top: 5px;' src='{0}'>
</a>
"""


class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage


class ApartmentAdmin(admin.ModelAdmin):
    readonly_fields = ('bulletin_images',)

    list_display = ('bullettin_url', 'address', 'price',
                    'latitude', 'longitude', 'status',
                    'created_at', 'updated_at', 'images_count')
    search_fields = ('address', 'price')
    exclude = ('created_at',)
    inlines = [ApartmentImageInline]

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

    def bulletin_images(self, obj):
        return format_html_join(
            mark_safe('<br/>'),
            IMAGE_TEMPLATE,
            ((i.image_url, ) for i in obj.images.all())
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(images_count=Count('images'))

    def images_count(self, obj):
        return obj.images_count

    images_count.admin_order_field = 'images_count'


class ApartmentImageAdmin(admin.ModelAdmin):
    pass


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
              )
    readonly_fields = fields
    list_display = ('time_started', 'time_finished', 'succeeded',
                    'total_saved', 'total_errors',
                    'time_taken')


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentImage, ApartmentImageAdmin)
admin.site.register(ApartmentScrapingResults, ApartmentScrapeStatsAdmin)
