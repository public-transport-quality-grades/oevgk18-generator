from typing import List, Dict, Optional
import logging
from .util.public_transport_group import PublicTransportGroup
from .util.public_transport_stop_category import PublicTransportStopCategory
from . import transport_stop_interval_retriever as interval_retriever
from .model.transport_stop import TransportStop

logger = logging.getLogger(__name__)

TransportGroups = Dict[int, PublicTransportGroup]
Intervals = Dict[int, Optional[float]]
TransportStopCategories = Dict[int, PublicTransportStopCategory]


def calculate_transport_stop_ratings(registry, due_date_config: dict,
                                     transport_stops: List[TransportStop]) -> TransportStopCategories:

    transport_groups: TransportGroups = calculate_transport_groups(registry, transport_stops)

    intervals: Intervals = interval_retriever.get_transport_stop_intervals(registry, due_date_config, transport_stops)

    return calculate_transport_stop_categories(registry, transport_stops, transport_groups, intervals)


def calculate_transport_groups(
        registry, transport_stops: List[TransportStop]) -> TransportGroups:
    timetable_service = registry['timetable_service']
    db_config = registry['config']['database-connections']
    min_junction_directions = registry['config']['public-transport-types']['train-junction-min-directions']

    with timetable_service.db_connection(db_config) as db:
        return {stop.uic_ref: _calculate_transport_group(
            timetable_service, db, stop, min_junction_directions) for stop in transport_stops}


def calculate_transport_stop_categories(
        registry, transport_stops: List[TransportStop],
        transport_groups: TransportGroups, intervals: Intervals) -> TransportStopCategories:
    """Calculate the transport stop category (I - VII) of all transport stops"""
    category_config = registry['config']['transport-stop-categories']
    return {stop.uic_ref: _calculate_transport_stop_category(
        stop.uic_ref, category_config, transport_groups[stop.uic_ref], intervals[stop.uic_ref])
        for stop in transport_stops}


def _calculate_transport_group(
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


def _calculate_transport_stop_category(uic_ref: int, category_configs, transport_group: PublicTransportGroup,
                                       interval: Optional[float]) -> Optional[PublicTransportStopCategory]:
    print(f"Calculating {uic_ref}")
    transport_group_mapping: List[dict] = _find_interval_range(category_configs, interval)
    for mapping in transport_group_mapping:
        if transport_group.value in mapping:
            stop_category = PublicTransportStopCategory(mapping[transport_group.value])
            logger.debug(f"{uic_ref}: {stop_category}, interval {interval}, group: {transport_group}")
            print(f"{uic_ref}: {stop_category}, interval {interval}, group: {transport_group}")
            return PublicTransportStopCategory(mapping[transport_group.value])

    return None


def _find_interval_range(category_configs, interval: Optional[float]) -> List[dict]:
    """Finds the range the interval is in and returns the configured mappings to the TransportGroups"""
    if not interval:
        interval = float('inf')

    for interval_category in category_configs:
        min_interval = interval_category['min-interval'] if 'min-interval' in interval_category else 0
        max_interval = interval_category['max-interval'] if 'max-interval' in interval_category else float('inf')
        if min_interval < interval <= max_interval:
            return interval_category['transport-type-mappings']

    raise ValueError(f"Invalid transport stop rating configuration, "
                     f"interval {interval} doesn't fit into any category")
