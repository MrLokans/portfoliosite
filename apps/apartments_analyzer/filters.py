from django.utils.translation import ugettext_lazy as _

from django.contrib.admin import SimpleListFilter


class BasePriceFilter(SimpleListFilter):
    title = _('Price range')

    parameter_name = 'price_USD'

    PRICE_RANGES = ()

    def get_price_map(self):
        return {'{} - {} USD'.format(*prices): prices for prices in self.PRICE_RANGES}

    def lookups(self, request, model_admin):
        return (
            (formatted_range, formatted_range)
            for formatted_range in self.get_price_map()
        )

    def queryset(self, request, queryset):
        price_range = self.get_price_map().get(self.value())
        if price_range is not None:
            lower_price, higher_price = price_range
            search_kwargs = {
                '{}__gte'.format(self.parameter_name): lower_price,
                '{}__lte'.format(self.parameter_name): higher_price,
            }
            queryset = queryset.filter(**search_kwargs)
        return queryset


class RoomCountFilter(SimpleListFilter):
    title = _('apartment type')

    parameter_name = 'apartment_type'

    def lookups(self, request, model_admin):
        return (
            ('Комната', 'Комната'),
            ('1-комнатная квартира', '1-комнатная квартира'),
            ('2-комнатная квартира', '2-комнатная квартира'),
            ('3-комнатная квартира', '3-комнатная квартира'),
            ('4-комнатная квартира', '4-комнатная квартира'),
            ('5-комнатная квартира', '5-комнатная квартира'),
            ('6-комнатная квартира', '6-комнатная квартира'),
            ('Other', 'Other'),
        )

    def queryset(self, request, queryset):
        apartment_type = self.value()
        if apartment_type:
            queryset = queryset.filter(apartment_type=apartment_type)
        return queryset


class RentedPriceRangeFilter(BasePriceFilter):
    PRICE_RANGES = (
        (0, 100),
        (101, 200),
        (201, 300),
        (301, 400),
        (401, 500),
        (501, 600),
        (601, 700),
        (701, 1_000),
        (1_001, 1_500),
        (1_501, 2_000),
        (2_001, 10_000),
    )


class SoldPriceRangeFilter(BasePriceFilter):
    PRICE_RANGES = (
        (0, 30_000),
        (30_001, 50_000),
        (50_001, 70_000),
        (70_001, 90_000),
        (90_001, 110_000),
        (110_001, 130_000),
        (130_001, 10_000_000),
    )
