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
