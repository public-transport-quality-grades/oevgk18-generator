from shapely.geometry import Polygon

from ...context import generator


def fake_isochrone(distance: float):
    return generator.business.model.isochrone.Isochrone(distance, Polygon())
