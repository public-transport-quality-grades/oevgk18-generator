from shapely.geometry import Point

from generator.business.model.transport_stop import TransportStop


def mock_transport_stops():
    stop1 = TransportStop('Zürich Oerlikon, Bahnhof', 8580449, False, Point(8.544790, 47.411496), [])
    stop2 = TransportStop('Zürich, Sternen Oerlikon', 8591382, False, Point(8.546231, 47.410070), [])
    return [stop1, stop2]
