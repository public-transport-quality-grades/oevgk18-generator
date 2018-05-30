from shapely.geometry import Point

from generator.business.model.transport_stop import TransportStop


def mock_transport_stops():
    stop1 = TransportStop('Zürich Oerlikon, Bahnhof', 8580449, Point(47.411496, 8.544790), [])
    stop2 = TransportStop('Zürich, Sternen Oerlikon', 8591382, Point(47.410070, 8.546231), [])
    return [stop1, stop2]
