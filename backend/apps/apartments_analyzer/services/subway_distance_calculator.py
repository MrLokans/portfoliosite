import itertools
from collections import namedtuple
from typing import List, Tuple

from tqdm import tqdm
from vincenty import vincenty

from apps.apartments_analyzer.models import (
    RentApartment,
    SoldApartments,
)
from apps.apartments_analyzer.constants import SUBWAY_DISTANCES_FIELD
from apps.apartments_analyzer.services.subway_data import SUBWAY_DATA

SubwayDistance = namedtuple("SubwayDistance", "name distance")
Point = namedtuple("Point", "latitude longitude")


SUBWAY_POINTS = [
    (subway_station, coords) for subway_station, coords in SUBWAY_DATA.items()
]
METERS_IN_KM = 1000


class ApartmentDistanceEnricher:
    def __init__(self, show_progress: bool = True):
        self.show_progress = show_progress

    def update_distance_data_for_apartments(self):
        rent_count = RentApartment.objects.with_non_filled_subway_distance().count()
        sold_count = SoldApartments.objects.with_non_filled_subway_distance().count()
        total_apartments = rent_count + sold_count
        apartments = itertools.chain(
            RentApartment.objects.with_non_filled_subway_distance(),
            SoldApartments.objects.with_non_filled_subway_distance(),
        )
        with tqdm(total=total_apartments, disable=not self.show_progress) as counter:
            for apartment in apartments:
                apartment = self.add_subway_distance_to_apartment(apartment)
                apartment.save()
                counter.update(1)

    def add_subway_distance_to_apartment(self, apartment):
        distances = self.get_subway_distances_for_coordinate(
            latitude=float(apartment.location.x), longitude=float(apartment.location.y)
        )
        apartment.subway_distances = {
            SUBWAY_DISTANCES_FIELD: [
                {"subway": subway, "distance": distance * METERS_IN_KM}
                for subway, distance in distances
            ]
        }
        return apartment

    def distance_between_points(
        self, point_1: Tuple[float, float], point_2: Tuple[float, float]
    ) -> float:
        return vincenty(point_1, point_2)

    def get_subway_distances_for_coordinate(
        self, latitude: float, longitude: float
    ) -> List[SubwayDistance]:
        """
        Return list of subways sorted by relative distance
        from given point (first ones are closer)
        """
        point_of_interest = (latitude, longitude)
        distances = [
            (
                station,
                self.distance_between_points(point_of_interest, subway_coordinates),
            )
            for station, subway_coordinates in SUBWAY_POINTS
        ]
        return sorted(distances, key=lambda x: x[1])
