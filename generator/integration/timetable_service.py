from datetime import datetime, timedelta
from typing import List
from contextlib import contextmanager
from records import Database


@contextmanager
def db_connection(db_config: dict):
    connection = Database(db_config['public-transport-stops'])
    yield connection
    connection.close()


def get_count_of_distinct_next_stops(db_config: dict, uic_ref: str) -> int:
    with db_connection(db_config) as db:
        rows = db.query("""SELECT nsm2.stop_name FROM next_station_mapping nsm1
                              INNER JOIN next_station_mapping nsm2 ON nsm1.trip_id = nsm2.trip_id
                              WHERE nsm1.parent_station = :uic_ref AND
                                  nsm1.stop_sequence = (nsm2.stop_sequence - 1)
                                  GROUP BY nsm2.stop_name;""", uic_ref=uic_ref).all()
        return len(rows)


def get_departure_times(db: Database, uic_ref: str, due_date: datetime) -> List[datetime]:
    due_date_gtfs: str = _format_gtfs_date(due_date)
    rows = db.query("""SELECT st.departure_time FROM stop_times st
                INNER JOIN stops s on st.stop_id = s.stop_id
                INNER JOIN trips t ON st.trip_id = t.trip_id
                INNER JOIN calendar_dates c ON t.service_id = c.service_id
                WHERE (st.stop_id = :uic_ref OR s.parent_station = :uic_ref) AND c.date = :date
                ORDER BY st.departure_time;""", uic_ref=uic_ref, date=due_date_gtfs).all()

    return list(map(lambda row: _parse_departure_times(row, due_date), rows))


def _format_gtfs_date(due_date: datetime) -> str:
    """Format datetime into gtfs date format yyymmdd"""
    return f"{due_date.year}{due_date.month:02d}{due_date.day:02d}"


def _parse_departure_times(row: dict, due_date: datetime) -> datetime:
    """convert row of departure time with format hh:mm:ss to time object"""
    hours, minutes, seconds = row['departure_time'].split(':')
    if hours == '24':
        # GTFS uses 24 as midnight, but python only knows 0..23, so we need to add one day
        due_date += timedelta(days=1)
        hours = 0

    return due_date.replace(hour=hours, minute=minutes, second=seconds)