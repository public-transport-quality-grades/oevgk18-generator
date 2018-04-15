from shapely.geometry import Point


class TransportPlatform:

    def __init__(self, osm_id: int, node_geom: Point):
        self.osm_id = osm_id
        self.node_geom = node_geom

    def __repr__(self):
        return f"{{osm_id: {self.osm_id}, node_geom: {self.node_geom}}}"
