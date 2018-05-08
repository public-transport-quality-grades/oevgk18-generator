from typing import List, Dict
import logging
from .util.public_transport_stop_category import PublicTransportStopCategory
from .util.public_transport_group import PublicTransportGroup
from ..business.model.isochrone import Isochrone
from ..business.model.grading import Grading
from . import transport_stop_rating_calculator, walking_time_retriever, transport_group_retriever
from . import transport_stop_grade_calculator

logger = logging.getLogger(__name__)

TransportStopCategories = Dict[int, PublicTransportStopCategory]
Isochrones = Dict[int, List[Isochrone]]
TransportStopGradings = Dict[int, List[Grading]]
TransportGroups = Dict[int, PublicTransportGroup]


def start(registry: dict, params):
    cli = registry['ui']
    cli.parse_params(params)
    output_writer = registry['output_writer']
    config = registry['config']

    walking_time_retriever.prepare_routing_table(registry)
    transport_groups: TransportGroups = transport_group_retriever.calculate_transport_groups(registry)

    for due_date_config in config['due-dates']:
        transport_ratings: TransportStopCategories = \
            transport_stop_rating_calculator.calculate_transport_stop_ratings(
                registry, due_date_config, transport_groups)

        stop_gradings: TransportStopGradings = transport_stop_grade_calculator.calculate_transport_stop_grades(
            registry, transport_ratings)

        output_writer.write_gradings(config['output'], due_date_config, stop_gradings)

        gradings_with_isochrones = [(uic_ref, gradings) for uic_ref, gradings in stop_gradings.items()
                                    if gradings]

        logger.debug(f"Found {len(gradings_with_isochrones)} stops with isochrones")
