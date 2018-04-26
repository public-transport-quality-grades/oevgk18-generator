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


def prepare_calendar_table(db: Database, due_date: datetime):
    """Setup table to use in get_departure_times for a specific date"""
    due_date_gtfs: str = _format_gtfs_date(due_date)
    db.query("TRUNCATE calendar_trip_mapping;")
    db.query("""INSERT INTO calendar_trip_mapping(departure_time, stop_id)
                    SELECT st.departure_time, st.stop_id FROM stop_times st
                        INNER JOIN trips t ON st.trip_id = t.trip_id
                        INNER JOIN calendar_dates c ON t.service_id = c.service_id
                        WHERE c.date = :date""", date=due_date_gtfs)


def get_departure_times(db: Database, uic_ref: str, due_date: datetime) -> List[datetime]:
    rows = db.query("""SELECT departure_time FROM calendar_trip_mapping
                WHERE stop_id like :uic_ref
                ORDER BY departure_time;""", uic_ref=f"{uic_ref}%").all()
    return list(map(lambda row: _combine_departure_time(row, due_date), rows))


def _format_gtfs_date(due_date: datetime) -> str:
    """Format datetime into gtfs date format yyymmdd"""
    return f"{due_date.year}{due_date.month:02d}{due_date.day:02d}"


def _combine_departure_time(row: dict, due_date: datetime) -> datetime:
    """Convert row of departure time with due date to form a complete datetime object"""
    departure_time: timedelta = row['departure_time']
    return due_date + departure_time
