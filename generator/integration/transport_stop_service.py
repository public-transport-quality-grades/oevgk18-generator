import logging
from typing import List
from contextlib import contextmanager
from records import Database, Record
from shapely.geometry import Point

from ..business.model.transport_stop import TransportStop

logger = logging.getLogger(__name__)


@contextmanager
def db_connection(db_config: dict):
    connection = Database(db_config['public-transport-stops'])
    yield connection
    connection.close()


def get_transport_stops(db: Database) -> List[TransportStop]:
    stop_rows = _query_transport_stop_rows(db)
    return list(map(_map_transport_stop, stop_rows))


def _query_transport_stop_rows(db: Database):
    return db.query("""SELECT DISTINCT
                          s.uic_ref,
                          s.stop_name,
                          s.stop_lat,
                          s.stop_lon,
                          array_agg(r.route_type)
                          OVER (PARTITION BY s.uic_ref) AS route_types,
                          (s.uic_ref IN (SELECT uic_ref FROM intercity_stations)) as is_intercity_station
                        FROM stops s
                          INNER JOIN stop_times st ON s.stop_id = st.stop_id
                          INNER JOIN trips t ON st.trip_id = t.trip_id
                          INNER JOIN routes r ON t.route_id = r.route_id
                        WHERE s.stop_id LIKE '85%'
                        GROUP BY s.uic_ref, s.stop_name, s.stop_lat, s.stop_lon, r.route_type;
                        """).all()


def _map_transport_stop(row: Record) -> TransportStop:
    uic_name = row['stop_name']
    uic_ref = int(row['uic_ref'])
    location = Point(row['stop_lon'], row['stop_lat'])
    route_types = row['route_types']
    is_intercity_station = row['is_intercity_station']
    if route_types == [None]:
        route_types = []

    return TransportStop(uic_name, uic_ref, is_intercity_station, location, route_types)
