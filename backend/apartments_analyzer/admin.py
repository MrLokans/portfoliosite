from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from apartments_analyzer.models import Apartment, ApartmentImage


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


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentImage, ApartmentImageAdmin)
