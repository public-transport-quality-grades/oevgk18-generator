from shapely import wkb
from shapely.geometry import Point


def parse_point_geometry(geom: str) -> Point:
    point: Point = wkb.loads(geom, hex=True)
    if point.is_valid:
        return point
    raise ValueError("Invalid point geometry")
