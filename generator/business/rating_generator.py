from typing import List, Dict
import logging
from .util.public_transport_stop_category import PublicTransportStopCategory
from ..business.model.isochrone import Isochrone
from ..business.model.grading import Grading
from . import transport_stop_rating_calculator, walking_time_retriever
from . import transport_stop_grade_calculator

logger = logging.getLogger(__name__)

TransportStopCategories = Dict[int, PublicTransportStopCategory]
Isochrones = Dict[int, List[Isochrone]]
TransportStopGradings = Dict[int, List[Grading]]


def start(registry: dict, params):
    cli = registry['ui']
    cli.parse_params(params)
    for due_date_config in registry['config']['due-dates'][:1]:
        # TODO execute for all configurations
        transport_ratings = \
            transport_stop_rating_calculator.calculate_transport_stop_ratings(registry, due_date_config)

        walking_time_retriever.prepare_routing_table(registry)
        stop_gradings: TransportStopGradings = transport_stop_grade_calculator.calculate_transport_stop_grades(
            registry, transport_ratings)

        gradings_with_isochrones = [(uic_ref, gradings) for uic_ref, gradings in stop_gradings.items()
                                    if gradings]

        logger.debug(f"Gradings: {list(gradings_with_isochrones)}")
        logger.debug(f"Found {len(gradings_with_isochrones)} stops with isochrones")
