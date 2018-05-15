from typing import Dict, List
import logging
from .model.transport_stop import TransportStop
from .model.public_transport_group import PublicTransportGroup

logger = logging.getLogger(__name__)

TransportGroups = Dict[int, PublicTransportGroup]


def get_transport_groups(registry) -> TransportGroups:
    timetable_service = registry['timetable_service']
    transport_stop_service = registry['transport_stop_service']
    db_config = registry['config']['database-connections']
    min_junction_directions = registry['config']['public-transport-types']['train-junction-min-directions']

    logger.info(f"Calculate transport groups")
    with timetable_service.db_connection(db_config) as db:
        transport_stops: List[TransportStop] = transport_stop_service.get_transport_stops(db)

        railway_lines = list(filter(lambda stop: stop.is_railway_line(), transport_stops))
        other_lines = list(set(transport_stops) - set(railway_lines))

        direction_count_stop_mapping = \
            timetable_service.get_count_of_distinct_next_stops(db, [stop.uic_ref for stop in railway_lines])
        railway_groups = {railway_line.uic_ref:
                          _get_transport_group(railway_line, direction_count_stop_mapping[railway_line.uic_ref],
                                               min_junction_directions)
                          for railway_line in railway_lines}

        other_groups = {line.uic_ref: _get_transport_group(line) for line in other_lines}

        return {**other_groups, **railway_groups}


def _get_transport_group(transport_stop: TransportStop,
                         direction_count: int = 0, min_junction_directions: int = 0) -> PublicTransportGroup:
    if transport_stop.is_railway_line():
        if _is_railway_junction(direction_count, min_junction_directions):
            return PublicTransportGroup.A
        else:
            return PublicTransportGroup.B
    return PublicTransportGroup.C


def _is_railway_junction(railway_direction_count: int, min_directions: int) -> bool:
    return railway_direction_count >= min_directions