from typing import List, Dict, Optional
import logging
from .util.public_transport_group import PublicTransportGroup
from .util.public_transport_stop_category import PublicTransportStopCategory
from . import transport_stop_interval_retriever as interval_retriever

logger = logging.getLogger(__name__)

TransportGroups = Dict[int, PublicTransportGroup]
Intervals = Dict[int, Optional[float]]
TransportStopCategories = Dict[int, PublicTransportStopCategory]


def calculate_transport_stop_ratings(
        registry, due_date_config: dict, transport_groups: TransportGroups) -> TransportStopCategories:

    intervals: Intervals = \
        interval_retriever.get_transport_stop_intervals(registry, due_date_config, [*transport_groups])

    return _calculate_transport_stop_categories(registry, transport_groups, intervals)


def _calculate_transport_stop_categories(
        registry, transport_groups: TransportGroups, intervals: Intervals) -> TransportStopCategories:
    """Calculate the transport stop category (I - VII) of all transport stops"""
    category_config = registry['config']['transport-stop-categories']
    return {stop_uic_ref: _calculate_transport_stop_category(
        stop_uic_ref, category_config, transport_groups[stop_uic_ref], intervals[stop_uic_ref])
        for stop_uic_ref in [*transport_groups]}


def _calculate_transport_stop_category(uic_ref: int, category_configs, transport_group: PublicTransportGroup,
                                       interval: Optional[float]) -> Optional[PublicTransportStopCategory]:
    logger.info(f"Calculating {uic_ref}")
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
