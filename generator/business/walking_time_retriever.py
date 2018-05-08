from typing import List, Dict
from .model.isochrone import Isochrone
from .util.public_transport_stop_category import PublicTransportStopCategory
from .util.public_transport_stop_grade import PublicTransportStopGrade

DistanceGradeMapping = Dict[float, PublicTransportStopGrade]


def prepare_routing_table(registry):
    routing_engine_service = registry['routing_engine_service']
    config = registry["config"]
    db_config = config['database-connections']
    with routing_engine_service.db_connection(db_config) as db:
        max_relevant_distance = config["isochrones"][0]["max-relevant-distance"]
        routing_engine_service.calc_effective_kilometres(db, max_relevant_distance)


def get_isochrones(registry, db, uic_ref: int, boundaries: List[float]) -> List[Isochrone]:
    routing_engine_service = registry['routing_engine_service']

    return routing_engine_service.calc_isochrones(db, uic_ref, boundaries)


def get_distance_grade_mapping(
        config: dict, stop_rating: PublicTransportStopCategory) -> DistanceGradeMapping:
    """Determine which walking times (= isochrone distance) with which grades have to be calculated"""
    distance_grades = {}
    ratings_config: list = config['public-transport-ratings']

    for rating_config in ratings_config:
        mappings = rating_config['transport-stop-categories']
        distance = _convert_walking_time_to_distance(config, rating_config['max-seconds'])

        for mapping in mappings:
            if stop_rating.value in mapping:
                distance_grades[distance] = PublicTransportStopGrade(mapping[stop_rating.value])
                break

    return distance_grades


def _convert_walking_time_to_distance(config, walking_time: int) -> float:
    """Convert walking time in seconds to distance in meters"""
    walking_speed = config["isochrones"][0]["walking-speed"]
    return walking_speed * walking_time
