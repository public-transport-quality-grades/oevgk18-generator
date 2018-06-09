import logging
from contextlib import contextmanager
from datetime import datetime
from typing import List, Dict

from records import Database

logger = logging.getLogger(__name__)


@contextmanager
def db_connection(db_config: dict):
    connection = Database(db_config['public-transport-stops'])
    yield connection
    connection.close()


def get_count_of_distinct_next_stops(db: Database, relevant_stops: List[str]) -> Dict[int, int]:
    rows = db.query("""WITH relevant_stops AS (
                            SELECT unnest(:relevant_stops) AS uic_ref
                        ),
                        next_station_mapping AS (
                            SELECT DISTINCT
                              s.stop_name,
                              t.trip_id,
                              st.stop_sequence,
                              s.uic_ref
                            FROM stops s
                              INNER JOIN stop_times st ON s.stop_id = st.stop_id
                              INNER JOIN trips t ON st.trip_id = t.trip_id
                              INNER JOIN routes r ON t.route_id = r.route_id
                            WHERE r.route_type = 2 OR r.route_type = 1
                        )
                        SELECT distinct
                          nsm1.uic_ref,
                          COUNT(nsm2.stop_name)
                          OVER (PARTITION BY nsm1.uic_ref )
                        FROM relevant_stops
                          LEFT JOIN next_station_mapping nsm1 ON relevant_stops.uic_ref = nsm1.uic_ref
                          INNER JOIN next_station_mapping nsm2 ON nsm1.trip_id = nsm2.trip_id
                        WHERE nsm1.stop_sequence = (nsm2.stop_sequence - 1)
                        GROUP BY nsm1.uic_ref, nsm2.stop_name;""",
                    relevant_stops=relevant_stops).all()

    return {int(row['uic_ref']): row['count'] for row in rows}


def get_all_departure_times(db_config: dict, due_date: datetime) -> Dict[int, List[datetime]]:
    with db_connection(db_config) as db:
        departure_times: Dict[int, List[datetime]] = _query_stop_times_departures(db, due_date)
        stop_frequency_departures: Dict[int, List[datetime]] = _query_frequency_departure_times(db, due_date)

    for uic_ref, frequency_departures in stop_frequency_departures.items():
        if uic_ref in departure_times:
            departure_times[uic_ref].extend(frequency_departures)
        else:
            departure_times[uic_ref] = frequency_departures
    return departure_times


def _query_stop_times_departures(db: Database, due_date: datetime) -> Dict[int, List[datetime]]:
    due_date_gtfs: str = _format_gtfs_date(due_date)
    rows = db.query("""WITH calendar_trip_mapping AS (
                            SELECT
                              st.departure_time,
                              s.uic_ref
                            FROM stop_times st
                              INNER JOIN stops s ON st.stop_id = s.stop_id
                              INNER JOIN trips t ON st.trip_id = t.trip_id
                              LEFT JOIN calendar_dates c ON t.service_id = c.service_id
                            WHERE NOT EXISTS(SELECT 1
                                             FROM frequencies f
                                             WHERE f.trip_id = t.trip_id) 
                                  AND (c.date = :date OR t.service_id = '000000')
                        )
                        SELECT
                          uic_ref,
                          array_agg(departure_time) AS departure_times
                        FROM calendar_trip_mapping
                        GROUP BY uic_ref""",
                    date=due_date_gtfs).all()
    # service_id 000000 represents the whole schedule
    return {row['uic_ref']: _combine_departure_time(row, due_date) for row in rows}


def _query_frequency_departure_times(db: Database, due_date: datetime) -> Dict[int, List[datetime]]:
    """Get departure times for stops which have trips that are modeled in the frequencies table"""
    due_date_gtfs: str = _format_gtfs_date(due_date)
    rows = db.query("""SELECT
                    s.uic_ref,
                    array_agg(st.departure_time + (INTERVAL '1s' * intervals)) AS departure_times
                  FROM stop_times st
                    INNER JOIN frequencies f on st.trip_id = f.trip_id
                    INNER JOIN trips t on f.trip_id = t.trip_id
                    INNER JOIN stops s on st.stop_id = s.stop_id
                    LEFT JOIN calendar_dates c ON t.service_id = c.service_id,
                  generate_series(0, 86400, f.headway_secs) intervals

                  WHERE (st.departure_time + (INTERVAL '1s' * intervals)) <= f.end_time
                    AND (c.date = :date OR t.service_id = '000000')
                  GROUP BY s.uic_ref""",
                    date=due_date_gtfs).all()
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
