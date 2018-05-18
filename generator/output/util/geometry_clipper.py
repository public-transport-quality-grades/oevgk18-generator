from typing import List, Dict
import rtree
from shapely.errors import TopologicalError
import logging

from . import make_valid, round_geometry
from ...business.model.grading import Grading
from ...business.model.stop_grade import StopGrade

logger = logging.getLogger(__name__)

TransportStopGradings = Dict[int, List[Grading]]


def clip_polygons(feature_map: List[dict]) -> List[dict]:
    """
    Clip polygons from other polygons in the same or lower class.
    E.g. polygons of grade A will be cut out from polygons of grade A or grade B.
    """
    clipped_features: Dict[int, dict] = {i: feature for i, feature in enumerate(feature_map)}
    index = _create_spatial_index(clipped_features)
    grades = list(reversed([grade.name for grade in StopGrade]))

    for i, grade in enumerate(grades):
        grade_filtered_features = {k: v for (k, v) in clipped_features.items()
                                   if v['properties']['grade'] == grade and not v['geometry'].is_empty}
        for relevant_feature in grade_filtered_features.values():
            for index_id in _search_index(index, relevant_feature):
                intersected_feature = clipped_features[index_id]
                if _is_same_feature(relevant_feature, intersected_feature) or \
                        intersected_feature['properties']['grade'] not in grades[:i+1]:
                    continue

                clipped_geom = _clip_geometry(relevant_feature['geometry'], intersected_feature['geometry'])

                if clipped_geom.is_empty:
                    _delete_index(index, index_id, intersected_feature['geometry'])
                else:
                    _update_index(index, index_id, intersected_feature['geometry'], clipped_geom)

                intersected_feature['geometry'] = clipped_geom

    return list(filter(lambda feature: not feature['geometry'].is_empty, clipped_features.values()))


def _clip_geometry(base_geometry, intersected_geometry):
    try:
        return intersected_geometry.difference(base_geometry)
    except TopologicalError:
        logger.debug(f"Geometry {base_geometry} or {intersected_geometry} is invalid")
        logger.debug(f"Base valid: {base_geometry.is_valid}, intersected valid: {intersected_geometry.is_valid}")
        try:
            rounded_intersected_geometry = round_geometry.round_geometry_coordinates(intersected_geometry)
            rounded_base_geometry = round_geometry.round_geometry_coordinates(base_geometry)

            cleaned_intersected_geometry = make_valid.make_geom_valid(rounded_intersected_geometry.buffer(0))
            cleaned_base_geometry = make_valid.make_geom_valid(rounded_base_geometry.buffer(0))
            return cleaned_intersected_geometry.difference(cleaned_base_geometry)
        except TopologicalError:
            logger.debug(f"Geometry still invalid: {cleaned_base_geometry} or {cleaned_intersected_geometry}")
            return base_geometry


def _create_spatial_index(feature_map: Dict[int, dict]):
    """ create rtree index for fast intersection checking """
    idx = rtree.index.Index()
    for i, feature in feature_map.items():
        idx.insert(i, feature['geometry'].bounds)
    return idx


def _search_index(index, feature: dict):
    """ search rtree index and return geometries that intersect with the feature """
    if feature['geometry'].is_empty:
        return []
    try:
        return map(lambda i: i, index.intersection(feature['geometry'].bounds))
    except rtree.core.RTreeError as e:
        logger.error(feature, e)


def _update_index(index, index_id, old_geom, geom):
    _delete_index(index, index_id, old_geom)
    index.insert(index_id, geom.bounds)


def _delete_index(index, index_id, geom):
    index.delete(index_id, geom.bounds)


def _is_same_feature(feature_a, feature_b):
    return feature_a['properties']['uic_ref'] == feature_b['properties']['uic_ref'] and \
           feature_a['properties']['grade'] == feature_b['properties']['grade']
