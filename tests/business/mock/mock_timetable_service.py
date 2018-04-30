from contextlib import contextmanager
from typing import List
from datetime import datetime

mocked_directions_values = {
    '8503400': 9,
    '8503125': 5,
    '8591382': 0
}

mocked_departure_times = {
    '8503400': [datetime(2018, 4, 23, 6, 35), datetime(2018, 4, 23, 7, 15)],

    '8503125': [datetime(2018, 4, 23, 9, 0), datetime(2018, 4, 23, 9, 15), datetime(2018, 4, 23, 9, 30),
                datetime(2018, 4, 23, 9, 45), datetime(2018, 4, 23, 10, 0), datetime(2018, 4, 23, 10, 15),
                datetime(2018, 4, 23, 10, 30), datetime(2018, 4, 23, 10, 45), datetime(2018, 4, 23, 11, 0),
                datetime(2018, 4, 23, 11, 15), datetime(2018, 4, 23, 11, 30), datetime(2018, 4, 23, 11, 45),
                datetime(2018, 4, 23, 12, 0), datetime(2018, 4, 23, 12, 15), datetime(2018, 4, 23, 12, 30),
                datetime(2018, 4, 23, 12, 45), datetime(2018, 4, 23, 13, 0), datetime(2018, 4, 23, 13, 15),
                datetime(2018, 4, 23, 13, 30), datetime(2018, 4, 23, 13, 45), datetime(2018, 4, 23, 14, 0),
                datetime(2018, 4, 23, 14, 15), datetime(2018, 4, 23, 14, 30), datetime(2018, 4, 23, 14, 45),
                datetime(2018, 4, 23, 15, 0), datetime(2018, 4, 23, 15, 15), datetime(2018, 4, 23, 15, 30),
                datetime(2018, 4, 23, 15, 45), datetime(2018, 4, 23, 16, 0), datetime(2018, 4, 23, 16, 15),
                datetime(2018, 4, 23, 16, 30), datetime(2018, 4, 23, 16, 45)],

    '8591382': [datetime(2018, 4, 23, 9, 1), datetime(2018, 4, 23, 9, 2), datetime(2018, 4, 23, 10, 1),
                datetime(2018, 4, 23, 10, 2), datetime(2018, 4, 23, 11, 0), datetime(2018, 4, 23, 11, 5)]
}


@contextmanager
def db_connection(db_config: dict):
    yield None


def get_count_of_distinct_next_stops(db_config: dict, uic_ref: str) -> int:
    return mocked_directions_values[uic_ref]


def get_departure_times(db, uic_ref: str, due_date: datetime) -> List[datetime]:
    return mocked_departure_times[uic_ref]


def prepare_calendar_table(db, due_date: datetime):
    pass
