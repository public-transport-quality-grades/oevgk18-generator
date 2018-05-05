import geojson
from typing import List
from ...business.model.isochrone import Isochrone


def write_geojson(geometries, filename: str):
    """ write geojson from a list of shapely geometries """
    features = [geojson.Feature(geometry=geom) for geom in geometries]
    feature_collection = geojson.FeatureCollection(features)
    with open(filename, 'w') as fp:
        geojson.dump(feature_collection, fp)


ISOCHRONE_COLOR = {
    420.0: '#700038',
    630.0: '#9966FF',
    840.0: '#00B000',
    1260.0: '#B3FF40'
}


def write_isochrone(isochrones: List[Isochrone], filename: str):
    if len(isochrones) == 0: return
    features = []

    for isochrone in reversed(isochrones):
        features.append(geojson.Feature(geometry=isochrone.polygon, properties={'distance': isochrone.distance},
                        style={
                            'fill': ISOCHRONE_COLOR[isochrone.distance],
                            'fill-opacity': 0.6
        }))
    feature_collection = geojson.FeatureCollection(features)
    with open(filename, 'w') as fp:
        geojson.dump(feature_collection, fp)
