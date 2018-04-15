from typing import Iterable
from contextlib import contextmanager
from records import Database, Record
from . import geometry_parser
from ..business.model.transport_stop import TransportStop
from ..business.model.transport_platform import TransportPlatform
from .. import config


@contextmanager
def db_connection():
    connection = Database(config.PTSTOP_DB_CONNECTION)
    yield connection
    connection.close()


def get_transport_stop_from_uic_ref(db: Database, uic_ref: str) -> TransportStop:
    pt_stop_rows = _query_transport_stop_node(db, uic_ref)
    return _map_transport_stop(uic_ref, pt_stop_rows)


def _query_transport_stop_node(db_connection: Database, uic_ref: str):
    return db_connection.query("SELECT id, tags, geom FROM pt_stop WHERE tags -> 'uic_ref' = :uic_ref", uic_ref=uic_ref)


def _map_transport_stop(uic_ref: str, rows: Iterable[Record]) -> TransportStop:
    platforms = list()
    uic_name = "undefined"
    for row in rows:
        if 'uic_name' in row.tags:
            uic_name = row.tags['uic_name']
        osm_id = row.id
        node_geom = geometry_parser.parse_point_geometry(row.geom)
        platforms.append(TransportPlatform(osm_id, node_geom))

    return TransportStop(uic_ref, uic_name, platforms)