from shapely.geometry import Polygon


class Isochrone:

    def __init__(self, distance: float, polygon: Polygon):
        self.distance: float = distance
        self.polygon: Polygon = polygon

    def __repr__(self):
        return f"{{distance: {self.distance}, polygon: {self.polygon}}}"
