from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.apartments_analyzer.filters import (
    RentedPriceRangeFilter,
    RoomCountFilter,
    SoldPriceRangeFilter,
    NearestSubwayStation, ActiveFilter)
from .models import RentApartment, ApartmentScrapingResults, SoldApartments, SUBWAY_DISTANCES_FIELD, AreaOfInterest, \
    UserSearchContact, UserSearch, SearchResults, CityRegion


class ApartmentsResource(resources.ModelResource):
    # pylint: disable=no-init
    class Meta:
        model = RentApartment


IMAGE_TEMPLATE = """
<a href='{0}' target='blank_'>
    <img style='width: 300px; padding-top: 5px;' src='{0}'>
</a>
"""

DISTANCE_TEMPLATE = """
<strong>{0}</strong> - <span>{1}</span>
"""


class BaseApartmentAdmin(OSMGeoAdmin):

    readonly_fields = ("bulletin_images", "subway_distances_list")
    list_display = (
        "bullettin_url",
        "address",
        "likely_agent",
        "price_USD",
        "price_BYN",
        "status",
        "location",
        "created_at",
        "updated_at",
        "images_count",
    )
    search_fields = ("address", "price_USD")

    def subway_distances_list(self, obj):
        distances = [(d['subway'], d['distance']) for d in obj.subway_distances.get(SUBWAY_DISTANCES_FIELD, [])]
        return format_html_join(mark_safe("<hr/>"), DISTANCE_TEMPLATE, distances)

    def bulletin_images(self, obj):
        return format_html_join(
            mark_safe("<br/>"),  # nosec
            IMAGE_TEMPLATE,
            ((link,) for link in obj.image_links),
        )

    def images_count(self, obj):
        return len(obj.image_links)

    images_count.admin_order_field = "images_count"


class ApartmentAdmin(BaseApartmentAdmin, ImportExportModelAdmin):

    list_filter = [RentedPriceRangeFilter, RoomCountFilter, NearestSubwayStation, ActiveFilter]

    resource_class = ApartmentsResource


class SoldApartmentAdmin(BaseApartmentAdmin, ImportExportModelAdmin):

    list_filter = [SoldPriceRangeFilter, NearestSubwayStation, ActiveFilter]


class ApartmentScrapeStatsAdmin(admin.ModelAdmin):
    fields = (
        "time_started",
        "time_finished",
        "succeeded",
        "error_message",
        "total_errors",
        "total_saved",
        "total_active",
        "total_inactive",
        "time_taken",
        "invalid_urls",
        "new_items",
        "updated_items",
    )
    readonly_fields = fields
    list_display = (
        "time_started",
        "time_finished",
        "succeeded",
        "total_saved",
        "total_errors",
        "time_taken",
    )


class CityRegionAdmin(OSMGeoAdmin):
    default_lon = 3068075
    default_lat = 7152226
    default_zoom = 11

    map_width = 800
    map_height = 600


class UserSearchContactAdmin(admin.ModelAdmin):
    pass


class UserSearchAdmin(admin.ModelAdmin):
    pass


class SearchResultsAdmin(admin.ModelAdmin):
    pass


class CityRegionAdmin(OSMGeoAdmin):
    pass


admin.site.register(AreaOfInterest, CityRegionAdmin)
admin.site.register(UserSearchContact, UserSearchContactAdmin)
admin.site.register(UserSearch, UserSearchAdmin)
admin.site.register(RentApartment, ApartmentAdmin)
admin.site.register(SoldApartments, SoldApartmentAdmin)
admin.site.register(ApartmentScrapingResults, ApartmentScrapeStatsAdmin)
admin.site.register(SearchResults, SearchResultsAdmin)
admin.site.register(CityRegion, CityRegionAdmin)

