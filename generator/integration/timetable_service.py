from datetime import datetime, timedelta
import logging
from typing import List, Dict
from contextlib import contextmanager
from records import Database

logger = logging.getLogger(__name__)


@contextmanager
def db_connection(db_config: dict):
    connection = Database(db_config['public-transport-stops'])
    yield connection
    connection.close()


def get_count_of_distinct_next_stops(db: Database) -> Dict[int, int]:
    rows =  db.query("""WITH relevant_stops AS (
                           SELECT s.stop_id
                               FROM stops s
                                  LEFT OUTER JOIN stops platforms on s.stop_id = platforms.parent_station
                               WHERE s.stop_id LIKE '85%' AND s.parent_station IS NULL
                                  GROUP BY s.stop_id
                       )
                       SELECT distinct nsm1.parent_station AS uic_ref, 
                          COUNT(nsm2.stop_name) OVER (PARTITION BY nsm1.parent_station)
                          FROM relevant_stops 
                              LEFT JOIN next_station_mapping nsm1 ON relevant_stops.stop_id = nsm1.parent_station
                              INNER JOIN next_station_mapping nsm2 ON nsm1.trip_id = nsm2.trip_id
                          WHERE nsm1.stop_sequence = (nsm2.stop_sequence - 1)
                              GROUP BY nsm1.parent_station, nsm2.stop_name;""").all()
    return {int(row['uic_ref']): row['count'] for row in rows}


def get_all_departure_times(db_config: dict, due_date: datetime) -> Dict[int, List[datetime]]:
    due_date_gtfs: str = _format_gtfs_date(due_date)
    with db_connection(db_config) as db:
        rows = db.query("""WITH calendar_trip_mapping AS (
                            SELECT st.departure_time, s.uic_ref
                            FROM stop_times st
                            INNER JOIN stops s ON st.stop_id = s.stop_id
                            INNER JOIN trips t ON st.trip_id = t.trip_id
                            INNER JOIN calendar_dates c ON t.service_id = c.service_id
                            WHERE c.date = :date
                          )
                          SELECT uic_ref, array_agg(departure_time) AS departure_times
                          FROM calendar_trip_mapping
                          GROUP BY uic_ref""", date=due_date_gtfs).all()
        return {row['uic_ref']: _combine_departure_time(row, due_date) for row in rows}


def _format_gtfs_date(due_date: datetime) -> str:
    """Format datetime into gtfs date format yyymmdd"""
    return f"{due_date.year}{due_date.month:02d}{due_date.day:02d}"


def _combine_departure_time(row: dict, due_date: datetime) -> List[datetime]:
    """Convert row of departure times with due date to form a complete datetime object"""
    departure_times: List[datetime] = list()
    for departure_time in row['departure_times']:
        if departure_time:
            departure_times.append(due_date + departure_time)

    return departure_times
