from typing import List, Dict
import logging
from .model.stop_category import StopCategory
from .model.public_transport_group import PublicTransportGroup
from .model.isochrone import Isochrone
from .model.grading import Grading
from . import stop_category_calculator, isochrone_retriever, transport_group_retriever, stop_grade_calculator

logger = logging.getLogger(__name__)

TransportStopCategories = Dict[int, StopCategory]
Isochrones = Dict[int, List[Isochrone]]
TransportStopGradings = Dict[int, List[Grading]]
TransportGroups = Dict[int, PublicTransportGroup]


def calculate_quality_grades(registry: dict, params):
    cli = registry['ui']
    cli.parse_params(params)
    output_writer = registry['output_writer']
    config = registry['config']

    isochrone_retriever.prepare_routing_table(registry)
    transport_groups: TransportGroups = transport_group_retriever.get_transport_groups(registry)

    for due_date_config in config['due-dates']:
        stop_categories: TransportStopCategories = \
            stop_category_calculator.get_stop_categories(
                registry, due_date_config, transport_groups)

        stop_gradings: TransportStopGradings = stop_grade_calculator.calculate_stop_grades(
            registry, stop_categories)

        output_writer.write_gradings(config['output'], due_date_config, stop_gradings)

        gradings_with_isochrones = [(uic_ref, gradings) for uic_ref, gradings in stop_gradings.items()
                                    if gradings]

        logger.debug(f"Found {len(gradings_with_isochrones)} stops with isochrones")
