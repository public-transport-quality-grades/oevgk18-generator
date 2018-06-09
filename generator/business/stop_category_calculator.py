import logging
from typing import List, Optional

from . import stop_interval_calculator
from .model.public_transport_group import PublicTransportGroup
from .model.stop_category import StopCategory
from ..types import TransportGroups, TransportStopCategories, Intervals

logger = logging.getLogger(__name__)


def get_stop_categories(
        registry, due_date_config: dict, transport_groups: TransportGroups) -> TransportStopCategories:
    intervals: Intervals = \
        stop_interval_calculator.calculate_stop_intervals(registry, due_date_config, [*transport_groups])

    return _calculate_stop_categories(registry, transport_groups, intervals)


def _calculate_stop_categories(
        registry, transport_groups: TransportGroups, intervals: Intervals) -> TransportStopCategories:
    """Calculate the transport stop category (I - VII) of all transport stops"""
    category_config = registry['config']['transport-stop-categories']
    return {
        stop.uic_ref: _calculate_stop_category(stop.uic_ref, category_config, transport_group, intervals[stop.uic_ref])
        for stop, transport_group in transport_groups.items()
    }


def _calculate_stop_category(uic_ref: int, category_configs, transport_group: PublicTransportGroup,
                             interval: Optional[float]) -> Optional[StopCategory]:
    logger.info(f"Calculating transport stop category for {uic_ref}")
    if not interval:
        return None
    transport_group_mapping: List[dict] = _find_interval_range(category_configs, interval)
    for mapping in transport_group_mapping:
        if transport_group.value in mapping:
            stop_category = StopCategory(mapping[transport_group.value])
            logger.debug(f"{uic_ref}: {stop_category}, interval {interval}, group: {transport_group}")
            return StopCategory(mapping[transport_group.value])

    return None


def _find_interval_range(category_configs, interval: float) -> List[dict]:
    """Finds the range the interval is in and returns the configured mappings to the TransportGroups"""
    for interval_category in category_configs:
        min_interval = interval_category['min-interval'] if 'min-interval' in interval_category else 0
        max_interval = interval_category['max-interval'] if 'max-interval' in interval_category else float('inf')
        if min_interval < interval <= max_interval:
            return interval_category['transport-type-mappings']

    raise ValueError(f"Invalid transport stop rating configuration, "
                     f"interval {interval} doesn't fit into any category")
