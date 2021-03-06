import logging
from typing import List

from .model.public_transport_group import PublicTransportGroup
from .model.transport_stop import TransportStop
from ..types import TransportGroups

logger = logging.getLogger(__name__)


def get_transport_groups(registry) -> TransportGroups:
    timetable_service = registry['timetable_service']
    transport_stop_service = registry['transport_stop_service']
    db_config = registry['config']['database-connections']
    min_junction_directions = registry['config']['public-transport-types']['train-junction-min-directions']

    logger.info(f"Calculate transport groups")
    with timetable_service.db_connection(db_config) as db:
        transport_stops: List[TransportStop] = transport_stop_service.get_transport_stops(db)

        railway_stations = list(filter(lambda stop: stop.is_railway_station(), transport_stops))
        other_stops = list(set(transport_stops) - set(railway_stations))

        direction_count_stop_mapping = \
            timetable_service.get_count_of_distinct_next_stops(db, [stop.uic_ref for stop in railway_stations])
        railway_groups = {
            railway_station: _get_transport_group(railway_station,
                                                  direction_count_stop_mapping[railway_station.uic_ref],
                                                  min_junction_directions)
            for railway_station in railway_stations
        }

        other_groups = {stop: _get_transport_group(stop) for stop in other_stops}

        return {**other_groups, **railway_groups}


def _get_transport_group(transport_stop: TransportStop,
                         direction_count: int = 0, min_junction_directions: int = 0) -> PublicTransportGroup:
    if transport_stop.is_railway_station():
        if _is_railway_junction(transport_stop, direction_count, min_junction_directions):
            return PublicTransportGroup.A
        else:
            return PublicTransportGroup.B
    return PublicTransportGroup.C


def _is_railway_junction(transport_stop: TransportStop, railway_direction_count: int, min_directions: int) -> bool:
    return transport_stop.is_intercity_station or railway_direction_count >= min_directions
