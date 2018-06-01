from typing import List
from generator.business.model.transport_stop import TransportStop, RouteType


def get_transport_stops(db) -> List[TransportStop]:
    return [
        TransportStop('', 8503400, False, None, [RouteType.RAIL.value, RouteType.SUBWAY.value]),
        TransportStop('', 8503125, False, None, [RouteType.RAIL.value, RouteType.SUBWAY.value]),
        TransportStop('', 8591382, False, None, [RouteType.BUS.value]),
        TransportStop('', 8593245, False, None, [RouteType.RAIL.value]),
        TransportStop('', 8504532, True, None, [RouteType.RAIL.value]),
    ]
