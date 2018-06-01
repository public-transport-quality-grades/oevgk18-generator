from typing import List
from shapely.geometry import Point

from .route_type import RouteType


class TransportStop:

    def __init__(self, uic_name: str, uic_ref: int, is_intercity_station: bool, location: Point,
                 route_types: List[int]):
        self.uic_name: str = uic_name
        self.uic_ref: int = uic_ref
        self.is_intercity_station: bool = is_intercity_station;
        self.location: Point = location
        self.route_types: List[RouteType] = [RouteType(route_type) for route_type in route_types]

    def is_railway_station(self) -> bool:
        return self.is_intercity_station or \
               any(route_type == RouteType.SUBWAY or route_type == RouteType.RAIL for route_type in self.route_types)

    def __repr__(self):
        return str(self.__dict__)
