from typing import Iterable, List
from contextlib import contextmanager
from records import Database, Record
from shapely.geometry import Point
from ..business.model.transport_stop import TransportStop


@contextmanager
def db_connection(db_config: dict):
    connection = Database(db_config['public-transport-stops'])
    yield connection
    connection.close()


def get_transport_stops(db_config: dict) -> List[TransportStop]:
    with db_connection(db_config) as db:
        pt_stop_rows = _query_transport_stop_rows(db)
        return list(map(_map_transport_stop, pt_stop_rows))


def _query_transport_stop_rows(db: Database):
    return db.query("""SELECT s.stop_id, s.stop_name, s.stop_lat, s.stop_lon, array_agg(platforms.platform_code)
                        AS platform
                       FROM stops s
                       LEFT OUTER JOIN stops platforms on s.stop_id = platforms.parent_station
                       WHERE s.stop_id LIKE '85%' AND s.parent_station IS NULL
                       GROUP BY s.stop_id;""")


def _map_transport_stop(row: Record) -> TransportStop:
    uic_name = row['stop_name']
    uic_ref = int(row['stop_id'])
    location = Point(row['stop_lon'], row['stop_lat'])
    platforms = row['platform']
    if platforms == [None]:
        platforms = []

    return TransportStop(uic_name, uic_ref, location, platforms)
