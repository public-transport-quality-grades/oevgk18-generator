import logging
from contextlib import contextmanager
from records import Database, Record
from typing import List, Optional
from .util import geometry_parser
from ..business.model.isochrone import Isochrone

logger = logging.getLogger(__name__)


@contextmanager
def db_connection(db_config: dict):
    connection = Database(db_config['public-transport-stops'])
    yield connection
    connection.close()


def mark_relevant_roads(db: Database, max_relevant_distance: float):
    logger.info(f"Mark nodes that are reachable in {max_relevant_distance} kilometres")
    transaction = db.transaction()
    db.query("""SELECT mark_relevant_ways(:max_relevant_distance);""", max_relevant_distance=max_relevant_distance)
    transaction.commit()


def split_routing_graph(db: Database):
    logger.info("Split routing graph into segments to improve accuracy")
    transaction = db.transaction()
    db.query("SELECT segment_routing_graph(10)")
    transaction.commit()


def optimize_stop_vertex_mapping(db: Database):
    logger.info("Locate public transport stops on the routing graph")
    transaction = db.transaction()
    db.query("SELECT optimize_stop_vertex_mapping()")
    transaction.commit()


def calc_effective_kilometres(db: Database):
    logger.info("Integrate terrain data into the routing graph")
    transaction = db.transaction()
    db.query("SELECT calc_effective_kilometres();")
    transaction.commit()


def calc_isochrones(db: Database, uic_ref: int, boundaries: List[int]) -> List[Isochrone]:
    logger.info(f"Calculate isochrones for {uic_ref}")

    nearest_vertex_id = _retrieve_nearest_vertex(db, uic_ref)
    if not nearest_vertex_id:
        return list()
    transaction = db.transaction()
    rows = db.query("""SELECT * FROM isochrones(:node_id, :boundaries)""",
                    node_id=nearest_vertex_id,
                    boundaries=boundaries
                    ).all()
    isochrones = _map_isochrones(rows)
    transaction.commit()
    return isochrones


def _retrieve_nearest_vertex(db: Database, uic_ref: int) -> Optional[int]:
    transaction = db.transaction()
    row = db.query("""SELECT nearest_vertex_id FROM stop_vertex_mapping
                       WHERE stop_uic_ref = :uic_ref;""", uic_ref=uic_ref).first()
    transaction.commit()
    if row:
        return row['nearest_vertex_id']
    return None


def _map_isochrones(rows: List[Record]) -> List[Isochrone]:
    return [Isochrone(float(row['distance']), geometry_parser.parse_polygon_geometry(row['polygon'])) for row in rows]
