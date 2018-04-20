from .util.public_transport_group import PublicTransportGroup


def calculate_transport_stop_rating(registry, uic_ref: str) -> PublicTransportGroup:
    timetable_service = registry['timetable_service']

    railway_direction_count = timetable_service.get_count_of_distinct_next_stops(uic_ref)
    if _is_railway_junction(railway_direction_count):
        return PublicTransportGroup.A
    if _is_railway(railway_direction_count):
        return PublicTransportGroup.B
    return PublicTransportGroup.C


def _is_railway_junction(railway_direction_count: int) -> bool:
    return railway_direction_count >= 6


def _is_railway(railway_direction_count: int) -> bool:
    return railway_direction_count > 0
