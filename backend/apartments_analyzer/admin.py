from django.contrib import admin
from django.db.models import Count

from apartments_analyzer.models import Apartment, ApartmentImage


class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('bullettin_url', 'address', 'price',
                    'latitude', 'longitude', 'status',
                    'created_at', 'updated_at', 'images_count')
    exclude = ('created_at',)
    inlines = [ApartmentImageInline]

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
