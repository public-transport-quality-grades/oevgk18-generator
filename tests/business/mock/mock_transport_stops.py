from shapely.geometry import Point
from generator.business.model.transport_stop import TransportStop, RouteType

stop_8503400 = TransportStop('', 8503400, False, Point(), [RouteType.RAIL.value, RouteType.SUBWAY.value])
stop_8503125 = TransportStop('', 8503125, False, Point(), [RouteType.RAIL.value, RouteType.SUBWAY.value])
stop_8591382 = TransportStop('', 8591382, False, Point(), [RouteType.BUS.value])
stop_8593245 = TransportStop('', 8593245, False, Point(), [RouteType.RAIL.value])
stop_8504532 = TransportStop('', 8504532, True, Point(), [RouteType.RAIL.value])
