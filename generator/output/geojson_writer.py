import logging
from itertools import chain
from os import path, makedirs
from typing import List

import geojson
from geojson import FeatureCollection, Feature
from shapely.geometry.base import BaseGeometry

from .util import round_geometry, filename_parser
from ..business.model.grading import Grading
from ..business.model.stop_grade import StopGrade
from ..business.model.transport_stop import TransportStop
from ..types import TransportStopGradings

logger = logging.getLogger(__name__)


def write_gradings(output_config: dict, due_date_config: dict, stop_gradings: TransportStopGradings):
    """ write geojson from a list of gradings """

    feature_map_list = [_build_grading_features(*stop_grading)
                        for stop_grading in stop_gradings.items()]

    feature_map: List[dict] = list(chain.from_iterable(feature_map_list))  # flatten list

    feature_map.sort(key=lambda feature: feature['properties']['grade'], reverse=True)

    features = list(map(lambda feature: Feature(**feature), feature_map))

    due_date_properties = _serialize_due_date(due_date_config)

    feature_collection = geojson.FeatureCollection(features=features, **due_date_properties)

    output_dir = output_config['output-directory']
    filename = filename_parser.get_filename_from_due_date_config(due_date_config)
    _write_geojson(output_dir, filename, feature_collection)


def write_transport_stops(output_config: dict, transport_stops: List[TransportStop]):
    """ write geojson from a list of transport stops """

    transport_stop_features = _build_stop_features(transport_stops)
    features = list(map(lambda feature: Feature(**feature), transport_stop_features))
    feature_collection = geojson.FeatureCollection(features=features)

    output_dir = output_config['output-directory']
    _write_geojson(output_dir, output_config['transport-stops-filename'], feature_collection)


def _build_grading_features(uic_ref: int, gradings: List[Grading]) -> List[dict]:
    return [_build_feature(round_geometry.round_geometry_coordinates(grading.isochrone.polygon),
                           _get_grading_properties(uic_ref, grading.grade))
            for grading in gradings]


def _build_stop_features(transport_stops: List[TransportStop]) -> List[dict]:
    return [_build_feature(stop.location,
                           _get_transport_stop_properties(stop.uic_name, stop.uic_ref))
            for stop in transport_stops]


def _build_feature(geometry: BaseGeometry, properties: dict) -> dict:
    return {
        'geometry': geometry,
        'properties': properties
    }


def _sort_gradings(gradings: List[Grading]) -> List[Grading]:
    """Sort gradings such that the innermost isochrone is rendered last"""
    return sorted(gradings, key=lambda grading: grading.isochrone.distance, reverse=True)


def _get_grading_properties(uic_ref: int, grade: StopGrade) -> dict:
    return {
        'uic_ref': uic_ref,
        'grade': grade.value,
    }


def _get_transport_stop_properties(uic_name: str, uic_ref: int) -> dict:
    return {
        'uic_name': uic_name,
        'uic_ref': uic_ref
    }


def _write_geojson(output_dir: str, filename: str, feature_collection: FeatureCollection):
    if not path.exists(output_dir):
        makedirs(output_dir)

    output_path = path.join(output_dir, filename)

    with open(output_path, 'w') as fp:
        geojson.dump(feature_collection, fp, separators=(',', ':'))  # eliminate whitespace by using custom separators


def _serialize_due_date(due_date_config: dict) -> dict:
    due_date_properties = due_date_config.copy()
    due_date_properties['due-date'] = due_date_config['due-date'].isoformat()
    return due_date_properties
