from shapely.geometry import Polygon


class Isochrone:

    def __init__(self, distance: float, polygon: Polygon):
        self.distance: float = distance
        self.polygon: Polygon = polygon

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
