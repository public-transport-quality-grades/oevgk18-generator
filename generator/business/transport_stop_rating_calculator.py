from typing import List
from .util.public_transport_group import PublicTransportGroup
from . import transport_stop_interval_retriever as interval_retriever


def calculate_transport_stop_ratings(registry, due_date_config: dict, uic_refs: List[str]):

    transport_groups = {uic_ref: calculate_transport_group(registry, uic_ref) for uic_ref in uic_refs}

    intervals: float = interval_retriever.get_transport_stop_intervals(registry, due_date_config, uic_refs)

    # TODO calculate transport stop category
    return intervals


def calculate_transport_group(registry, uic_ref: str) -> PublicTransportGroup:

    timetable_service = registry['timetable_service']
    db_config = registry['config']['database-connections']
    min_junction_directions = registry['config']['public-transport-types']['train-junction-min-directions']

    railway_direction_count = timetable_service.get_count_of_distinct_next_stops(db_config, uic_ref)
    if _is_railway_junction(railway_direction_count, min_junction_directions):
        return PublicTransportGroup.A
    if _is_railway(railway_direction_count):
        return PublicTransportGroup.B
    return PublicTransportGroup.C


def _is_railway_junction(railway_direction_count: int, min_directions: int) -> bool:
    return railway_direction_count >= min_directions


def _is_railway(railway_direction_count: int) -> bool:
    return railway_direction_count > 0
