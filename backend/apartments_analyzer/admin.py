from django.contrib import admin

from apartments_analyzer.models import Apartment


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('bullettin_url', 'address', 'price',
                    'latitude', 'longitude', 'status', )


admin.site.register(Apartment, ApartmentAdmin)
