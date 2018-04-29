from typing import List, Dict
import logging
from .util.public_transport_group import PublicTransportGroup
from . import transport_stop_interval_retriever as interval_retriever
from .model.transport_stop import TransportStop

logger = logging.getLogger(__name__)


def calculate_transport_stop_ratings(registry, due_date_config: dict, transport_stops: List[TransportStop]):

    transport_groups = calculate_transport_groups(registry, transport_stops)

    intervals: float = interval_retriever.get_transport_stop_intervals(registry, due_date_config, transport_stops)

    # TODO calculate transport stop category
    return intervals


def calculate_transport_groups(
        registry, transport_stops: List[TransportStop]) -> Dict[PublicTransportGroup, TransportStop]:
    timetable_service = registry['timetable_service']
    db_config = registry['config']['database-connections']
    min_junction_directions = registry['config']['public-transport-types']['train-junction-min-directions']

    with timetable_service.db_connection(db_config) as db:
        return {stop: calculate_transport_group(
            timetable_service, db, stop, min_junction_directions) for stop in transport_stops}


def calculate_transport_group(
        timetable_service, db, transport_stop: TransportStop, min_junction_directions: int) -> PublicTransportGroup:

    logger.debug(f"Calculate transport group for {transport_stop.uic_ref}")
    railway_direction_count = timetable_service.get_count_of_distinct_next_stops(db, transport_stop.uic_ref)
    if _is_railway_junction(railway_direction_count, min_junction_directions):
        return PublicTransportGroup.A
    if _is_railway(railway_direction_count):
        return PublicTransportGroup.B
    return PublicTransportGroup.C


def _is_railway_junction(railway_direction_count: int, min_directions: int) -> bool:
    return railway_direction_count >= min_directions


def _is_railway(railway_direction_count: int) -> bool:
    return railway_direction_count > 0
