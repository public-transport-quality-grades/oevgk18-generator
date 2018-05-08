from typing import Dict, List, Optional
import logging
from .util.public_transport_stop_category import PublicTransportStopCategory
from .util.public_transport_stop_grade import PublicTransportStopGrade
from . import walking_time_retriever
from .model.isochrone import Isochrone
from .model.grading import Grading

TransportStopCategories = Dict[int, PublicTransportStopCategory]
Isochrones = Dict[int, List[Isochrone]]
DistanceGradeMapping = Dict[float, PublicTransportStopGrade]
TransportStopGradings = Dict[int, List[Grading]]

logger = logging.getLogger(__name__)


def calculate_transport_stop_grades(
        registry, transport_ratings: TransportStopCategories) -> TransportStopGradings:

    routing_engine_service = registry['routing_engine_service']
    db_config = registry['config']['database-connections']

    with routing_engine_service.db_connection(db_config) as db:
        return {uic_ref: _calculate_grades_for_stop(registry, db, uic_ref, stop_rating)
                for uic_ref, stop_rating in transport_ratings.items() if stop_rating is not None}


def _calculate_grades_for_stop(
        registry, db, uic_ref: int, stop_rating: PublicTransportStopCategory) -> List[Grading]:

    logger.debug(f"Calculate gradings for {uic_ref}")
    config = registry['config']
    distance_grades: DistanceGradeMapping = walking_time_retriever.get_distance_grade_mapping(config, stop_rating)
    isochrones: List[Isochrone] = walking_time_retriever.get_isochrones(
        registry, db, uic_ref, [*distance_grades])
    gradings: List[Grading] = [grading for grading in [_map_isochrone_to_grading(isochrone, distance_grades)
                               for isochrone in isochrones] if grading is not None]
    logger.debug(f"Gradings for {uic_ref}: {gradings}")
    return gradings


def _map_isochrone_to_grading(
        isochrone: Isochrone, distance_grades: Dict[float, PublicTransportStopGrade]) -> Optional[Grading]:

    grade = list([grade for distance, grade in distance_grades.items() if distance == isochrone.distance])
    if grade:
        return Grading(isochrone, grade[0])
    return None
