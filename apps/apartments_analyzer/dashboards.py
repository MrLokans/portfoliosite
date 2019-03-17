from controlcenter import Dashboard, widgets

from apps.apartments_analyzer.models import SoldApartments, RentApartment
from apps.apartments_analyzer.services import ApartmentsStatisticsAggregator


class TotalCount(widgets.ItemList):

    def values(self):
        return [
            ['Sold', RentApartment.objects.count()],
            ['For rent', SoldApartments.objects.count()],
            ['Active to sell', RentApartment.objects.active().count()],
            ['Active for rent', SoldApartments.objects.active().count()],
        ]


class SoldPriceStats(widgets.ItemList):

    def values(self):
        return ApartmentsStatisticsAggregator.get_price_metrics_for_last_n_days()


class ApartmentsDashboard(Dashboard):
    widgets = (
        TotalCount,
        SoldPriceStats,
    )
