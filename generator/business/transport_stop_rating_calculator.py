from .util.public_transport_group import PublicTransportGroup


def calculate_transport_stop_rating(registry, uic_ref: str):

    transport_group: PublicTransportGroup = calculate_transport_group(registry, uic_ref)

    # TODO calculate transport stop rating
    return transport_group


def calculate_transport_group(registry, uic_ref: str) -> PublicTransportGroup:

    timetable_service = registry['timetable_service']
    db_config = registry['config']['database-connections']
    min_junction_directions = registry['config']['public-transport-types']['train-junction-min-directions']

    railway_direction_count = timetable_service.get_count_of_distinct_next_stops(db_config, uic_ref)
    if _is_railway_junction(railway_direction_count, min_junction_directions):
        return PublicTransportGroup.A
    if _is_railway(railway_direction_count):
        return PublicTransportGroup.B
    return PublicTransportGroup.C


def _is_railway_junction(railway_direction_count: int, min_directions: int) -> bool:
    return railway_direction_count >= min_directions


def _is_railway(railway_direction_count: int) -> bool:
    return railway_direction_count > 0
