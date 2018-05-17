from shapely.geometry import Polygon, shape, mapping
import logging

PRECISION = 5

logger = logging.getLogger(__name__)


def round_geometry_coordinates(geometry: Polygon) -> Polygon:
    """round coordinates of polygon to reduce topology error and geojson file size"""
    geojson_geom = mapping(geometry)
    _round_geojson_coordinates(geojson_geom)
    return shape(geojson_geom)


def _round_geojson_coordinates(geojson_geom: dict) -> None:
    if geojson_geom['type'] == 'GeometryCollection':
        for geometry in geojson_geom['geometries']:
            return _round_geojson_coordinates(geometry)

    geojson_geom['coordinates'] = list(map(_round_coordinates, geojson_geom['coordinates']))


def _round_coordinates(coords) -> list:
    """Adapted from https://github.com/perrygeo/geojson-precision"""
    result = []
    try:
        return round(coords, PRECISION)
    except TypeError:
        for coord in coords:
            result.append(_round_coordinates(coord))

    return result
