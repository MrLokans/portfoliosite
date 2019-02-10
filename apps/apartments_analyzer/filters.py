from django.utils.translation import ugettext_lazy as _

from django.contrib.admin import SimpleListFilter


class PriceRangeFilter(SimpleListFilter):
    title = _('Price range')

    parameter_name = 'price_USD'

    PRICE_RANGES = (
        (0, 100),
        (101, 200),
        (201, 300),
        (301, 400),
        (401, 500),
        (501, 600),
        (601, 700),
        (701, 1000),
        (1001, 1500),
        (1501, 2000),
        (2001, 10000),
    )
    PRICE_MAP = {'{} - {} USD'.format(*prices): prices for prices in PRICE_RANGES}

    def lookups(self, request, model_admin):
        return (
            (formatted_range, formatted_range)
            for formatted_range in self.PRICE_MAP
        )

    def queryset(self, request, queryset):
        price_range = self.PRICE_MAP.get(self.value())
        if price_range is not None:
            lower_price, higher_price = price_range
            queryset = queryset.filter(price_USD__gte=lower_price, price_USD__lte=higher_price)
        return queryset
