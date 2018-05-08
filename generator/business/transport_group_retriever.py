from typing import Dict
import logging
from .util.public_transport_group import PublicTransportGroup

logger = logging.getLogger(__name__)

TransportGroups = Dict[int, PublicTransportGroup]


def calculate_transport_groups(registry) -> TransportGroups:
    timetable_service = registry['timetable_service']
    db_config = registry['config']['database-connections']
    min_junction_directions = registry['config']['public-transport-types']['train-junction-min-directions']

    logger.info(f"Calculate transport groups")
    with timetable_service.db_connection(db_config) as db:
        direction_count_stop_mapping = timetable_service.get_count_of_distinct_next_stops(db)
        return {uic_ref: _calculate_transport_group(direction_count, min_junction_directions)
                for (uic_ref, direction_count) in direction_count_stop_mapping.items()}


def _calculate_transport_group(direction_count: int, min_junction_directions: int) -> PublicTransportGroup:
    if _is_railway_junction(direction_count, min_junction_directions):
        return PublicTransportGroup.A
    if _is_railway(direction_count):
        return PublicTransportGroup.B
    return PublicTransportGroup.C


def _is_railway_junction(railway_direction_count: int, min_directions: int) -> bool:
    return railway_direction_count >= min_directions


def _is_railway(railway_direction_count: int) -> bool:
    return railway_direction_count > 0
