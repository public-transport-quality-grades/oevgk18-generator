import logging
from contextlib import contextmanager
from records import Database, Record
from typing import List, Dict, Tuple
from .util import geometry_parser, geojson_writer
from ..business.model.isochrone import Isochrone

logger = logging.getLogger(__name__)


@contextmanager
def db_connection(db_config: dict):
    connection = Database(db_config['public-transport-stops'])
    yield connection
    connection.close()


def calc_effective_kilometres(db: Database, max_relevant_distance: float):
    _mark_relevant_roads(db, max_relevant_distance)
    logger.info(f"Calculate effective kilometres")
    transaction = db.transaction()
    db.query("SELECT calc_effective_kilometres();")
    transaction.commit()


def _mark_relevant_roads(db: Database, max_relevant_distance: float):
    logger.info(f"Mark nodes that are reachable in {max_relevant_distance} metres")
    transaction = db.transaction()
    db.query("""SELECT mark_relevant_ways(:max_relevant_distance);""", max_relevant_distance=max_relevant_distance)
    transaction.commit()


def calc_isochrones(db: Database, boundaries: List[int]) -> Dict[str, Isochrone]:
    stop_isochrones = {}
    for (uic_ref, nearest_vertex_id) in _retrieve_uic_ref_vertex_mapping(db):
        logger.info(f"Calculate isochrones for {uic_ref}")
        transaction = db.transaction()
        rows = db.query("""SELECT * FROM isochrones(:node_id, :boundaries)""",
                        node_id=nearest_vertex_id,
                        boundaries=boundaries
                        ).all()
        isochrones = _map_isochrones(rows)
        stop_isochrones[uic_ref] = isochrones
        transaction.commit()
    return stop_isochrones


def _retrieve_uic_ref_vertex_mapping(db: Database) -> List[Tuple[int, int]]:
    transaction = db.transaction()
    rows = db.query("""SELECT stop_uic_ref, nearest_vertex_id FROM stop_vertex_mapping;""").all()
    transaction.commit()
    return [(row['stop_uic_ref'], row['nearest_vertex_id']) for row in rows]


def _map_isochrones(rows: List[Record]) -> List[Isochrone]:
    return [Isochrone(float(row['distance']), geometry_parser.parse_polygon_geometry(row['polygon'])) for row in rows]
