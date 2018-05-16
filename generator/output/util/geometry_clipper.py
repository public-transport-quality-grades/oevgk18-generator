from typing import List, Dict
import rtree, shapely
import logging

from generator.business.model.grading import Grading
from generator.business.util.public_transport_stop_grade import PublicTransportStopGrade

logger = logging.getLogger(__name__)

TransportStopGradings = Dict[int, List[Grading]]


def clip_polygons(feature_map: List[dict]) -> List[dict]:
    """
    Clip polygons from other polygons in the same or lower class.
    E.g. polygons of grade A will be cut out from polygons of grade A or grade B.
    """
    clipped_features: Dict[int, dict] = {i: feature for i, feature in enumerate(feature_map)}
    index = _create_spatial_index(clipped_features)
    grades = list(reversed([grade.name for grade in PublicTransportStopGrade]))

    for i, grade in enumerate(grades):
        grade_filtered_features = {k: v for (k, v) in clipped_features.items()
                                   if v['properties']['grade'] == grade and not v['geometry'].is_empty}
        for relevant_feature in grade_filtered_features.values():
            for index_id in _search_index(index, relevant_feature):
                intersected_feature = clipped_features[index_id]
                if _is_same_feature(relevant_feature, intersected_feature) or \
                        intersected_feature['properties']['grade'] not in grades[:i+1]:
                    continue

                try:
                    clipped_geom = intersected_feature['geometry'].difference(relevant_feature['geometry'])

                    if clipped_geom.is_empty:
                        _delete_index(index, index_id, intersected_feature['geometry'])
                    else:
                        _update_index(index, index_id, intersected_feature['geometry'], clipped_geom)

                    intersected_feature['geometry'] = clipped_geom
                except shapely.errors.TopologicalError as e:
                    #  TODO solve issue
                    logging.error(intersected_feature, relevant_feature, e)
    return list(filter(lambda feature: not feature['geometry'].is_empty, clipped_features.values()))


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
