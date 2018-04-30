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


def get_count_of_distinct_next_stops(db: Database, uic_ref: int) -> int:
    rows = db.query("""SELECT nsm2.stop_name FROM next_station_mapping nsm1
                          INNER JOIN next_station_mapping nsm2 ON nsm1.trip_id = nsm2.trip_id
                          WHERE nsm1.parent_station = :uic_ref AND
                              nsm1.stop_sequence = (nsm2.stop_sequence - 1)
                              GROUP BY nsm2.stop_name;""", uic_ref=str(uic_ref)).all()
    return len(rows)


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
