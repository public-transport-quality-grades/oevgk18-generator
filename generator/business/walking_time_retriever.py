from typing import List


def get_isochrones(registry):
    routing_engine_service = registry['routing_engine_service']
    config = registry["config"]
    db_config = config['database-connections']
    with routing_engine_service.db_connection(db_config) as db:
        max_relevant_distance = config["isochrones"][0]["max-relevant-distance"]
        routing_engine_service.calc_effective_kilometres(db, max_relevant_distance)

        walking_speed = config["isochrones"][0]["walking-speed"]
        boundaries = _calc_boundaries(walking_speed, config["public-transport-ratings"])
        routing_engine_service.calc_isochrones(db, boundaries)


def _calc_boundaries(walking_speed: float, public_transport_ratings_config: dict) -> List[float]:
    boundaries = []
    for public_transport_rating_config in public_transport_ratings_config:
        max_distance = walking_speed * public_transport_rating_config['max-seconds']
        boundaries.append(max_distance)
    return boundaries
