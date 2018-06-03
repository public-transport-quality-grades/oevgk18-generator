from typing import Dict, List, Optional
import logging

from ..types import TransportStopCategories, TransportStopGradings, DistanceGradeMapping
from .model.stop_category import StopCategory
from .model.stop_grade import StopGrade
from .model.isochrone import Isochrone
from .model.grading import Grading
from . import isochrone_retriever


logger = logging.getLogger(__name__)


def prepare_calculation(registry: dict) -> None:
    isochrone_retriever.prepare_routing_table(registry)


def calculate_stop_grades(
        registry, transport_ratings: TransportStopCategories) -> TransportStopGradings:
    routing_engine_service = registry['routing_engine_service']
    db_config = registry['config']['database-connections']

    with routing_engine_service.db_connection(db_config) as db:
        transport_stop_gradings = {stop_uic_ref: _calculate_grades_for_stop(registry, db, stop_uic_ref, stop_rating)
                                   for stop_uic_ref, stop_rating in transport_ratings.items()
                                   if stop_rating is not None}
        return {uic_ref: gradings
                for uic_ref, gradings in transport_stop_gradings.items()
                if gradings}


def _calculate_grades_for_stop(
        registry, db, uic_ref: int, stop_rating: StopCategory) -> List[Grading]:

    logger.debug(f"Calculate gradings for {uic_ref}")
    config = registry['config']
    distance_grades: DistanceGradeMapping = isochrone_retriever.get_distance_grade_mapping(config, stop_rating)
    isochrones: List[Isochrone] = isochrone_retriever.get_isochrones(
        registry, db, uic_ref, [*distance_grades])
    gradings: List[Grading] = [grading for grading in [_map_isochrone_to_grading(isochrone, distance_grades)
                                                       for isochrone in isochrones] if grading is not None]
    logger.debug(f"Gradings for {uic_ref}: {gradings}")
    return gradings


def _map_isochrone_to_grading(
        isochrone: Isochrone, distance_grades: Dict[float, StopGrade]) -> Optional[Grading]:

    grade = list([grade for distance, grade in distance_grades.items() if distance == isochrone.distance])
    if grade:
        return Grading(isochrone, grade[0])
    return None
