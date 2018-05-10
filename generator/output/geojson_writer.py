from typing import List, Dict
import logging
from os import path, makedirs
from itertools import chain
import geojson
from geojson import FeatureCollection, Feature
from generator.business.model.grading import Grading
from generator.business.util.public_transport_stop_grade import PublicTransportStopGrade


logger = logging.getLogger(__name__)

TransportStopGradings = Dict[int, List[Grading]]


def write_gradings(output_config: dict, due_date_config: dict, stop_gradings: TransportStopGradings):
    """ write geojson from a list of shapely geometries """

    styling_config = output_config['styling']
    output_dir = output_config['output-directory']

    gradings_with_isochrones = {uic_ref: gradings for uic_ref, gradings in stop_gradings.items()
                                if gradings}

    feature_map_list = [_build_stop_features(styling_config, *stop_grading)
                    for stop_grading in gradings_with_isochrones.items()]

    feature_map: List[Feature] = list(chain.from_iterable(feature_map_list))  # flatten list

    feature_map.sort(key=lambda feature: feature['properties']['grade'], reverse=True)

    features = list(map(lambda feature: Feature(**feature), feature_map))

    due_date_properties = _serialize_due_date(due_date_config)

    feature_collection = geojson.FeatureCollection(features=features, **due_date_properties)

    _write_geojson(output_dir, due_date_config, feature_collection)


def _build_stop_features(styling_config: dict, uic_ref: int, gradings: List[Grading]) -> List[dict]:

    return [{
        'geometry': grading.isochrone.polygon,
        'properties': _get_feature_properties(styling_config, uic_ref, grading.grade)
    } for grading in gradings]


def _sort_gradings(gradings: List[Grading]) -> List[Grading]:
    """Sort gradings such that the innermost isochrone is rendered last"""
    return sorted(gradings, key=lambda grading: grading.isochrone.distance, reverse=True)


def _get_feature_properties(styling_config: dict, uic_ref: int, grade: PublicTransportStopGrade) -> dict:
    colors = styling_config['colors']
    if grade.value not in colors:
        logger.warning(f"No color defined for rating {grade.value}")
        color = "#FF0000"
    else:
        color = colors[grade.value]

    return {
        'uic_ref': uic_ref,
        'grade': grade.value,
        'fill': color,
        'fill-opacity': styling_config['opacity']
    }


def _write_geojson(output_dir: str, due_date_config: dict, feature_collection: FeatureCollection):
    filename = f"oevgk18_{due_date_config['due-date'].strftime('%Y-%m-%d')}_" \
               f"{due_date_config['type-of-interval']}.geojson"

    if not path.exists(output_dir):
        makedirs(output_dir)

    output_path = path.join(output_dir, filename)

    with open(output_path, 'w') as fp:
        geojson.dump(feature_collection, fp)


def _serialize_due_date(due_date_config: dict) -> dict:
    due_date_properties = due_date_config.copy()
    due_date_properties['due-date'] = due_date_config['due-date'].isoformat()
    return due_date_properties
