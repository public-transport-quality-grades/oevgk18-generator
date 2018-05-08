from shapely import wkb
from shapely.geometry import Polygon


def parse_polygon_geometry(geom: str) -> Polygon:
    polygon: Polygon = wkb.loads(geom, hex=True)
    if polygon.is_valid:
        return polygon
    raise ValueError("Invalid polygon geometry")
