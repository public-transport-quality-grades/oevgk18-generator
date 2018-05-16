import logging
import os
from contextlib import contextmanager
from records import Database, Record
from typing import List, Optional, Iterable
from concurrent.futures import ThreadPoolExecutor
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


def split_routing_graph(db: Database, edge_segment_length):
    logger.info(f"Split routing graph into segments of length {edge_segment_length}m to improve accuracy")
    transaction = db.transaction()
    db.query("SELECT segment_routing_graph(:segment_length)", segment_length=edge_segment_length)
    transaction.commit()


def optimize_stop_vertex_mapping(db: Database):
    logger.info("Locate public transport stops on the routing graph")
    transaction = db.transaction()
    db.query("SELECT optimize_stop_vertex_mapping()")
    transaction.commit()


def calc_effective_kilometres(db_config):
    logger.info("Integrate terrain data into the routing graph")
    cpu_count = os.cpu_count()
    with ThreadPoolExecutor() as executor:
        futures = []
        for start_id, end_id in _partition_effective_kilometres_calculation(db_config, cpu_count):
            logger.debug(f"Start task with ids from {start_id} to {end_id}")
            futures.append(executor.submit(_execute_calc_effective_kilometres, db_config, start_id, end_id))
        for future in futures:
            future.result()
            logger.debug("Task completed")


def _execute_calc_effective_kilometres(db_config, start_id: int, end_id: int) -> None:
    with db_connection(db_config) as db:
        transaction = db.transaction()
        try:
            db.query("SELECT calc_effective_kilometres(:start_id, :end_id);", start_id=start_id, end_id=end_id)
        except Exception as ex:
            logger.debug("Error in calc_effective_kilometres")
        transaction.commit()


def _partition_effective_kilometres_calculation(db_config, partitions: int) -> Iterable:
    with db_connection(db_config) as db:
        row_ids = db.query("SELECT id FROM routing_segmented ORDER BY id;").all()
        routing_ids: List[int] = list(map(lambda row: row.id, row_ids))

    row_count = len(routing_ids)
    start_index: int = 0
    for _ in range(partitions)[:-1]:
        end_index = start_index + int(row_count / partitions)
        yield routing_ids[start_index], routing_ids[end_index]
        start_index = end_index + 1
    yield routing_ids[start_index], routing_ids[-1]


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
