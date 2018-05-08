from contextlib import contextmanager
from typing import Dict, List
from datetime import datetime


mocked_return_values = {
    8503400: 9,
    8503125: 5,
    8591382: 0,
    8593245: 6
}


mocked_departure_times = {
    8503400: [datetime(2018, 4, 23, 6, 35), datetime(2018, 4, 23, 7, 15)],

    8503125: [datetime(2018, 4, 23, 9, 0), datetime(2018, 4, 23, 9, 15), datetime(2018, 4, 23, 9, 30),
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

    8591382: [datetime(2018, 4, 23, 9, 1), datetime(2018, 4, 23, 9, 2), datetime(2018, 4, 23, 10, 1),
              datetime(2018, 4, 23, 10, 2), datetime(2018, 4, 23, 11, 0), datetime(2018, 4, 23, 11, 5)]
}


@contextmanager
def db_connection(db_config: dict):
    yield None


def get_count_of_distinct_next_stops(db_config: dict) -> int:
    return mocked_return_values


def get_all_departure_times(db_config: dict, due_date: datetime) -> Dict[int, List[datetime]]:
    return mocked_departure_times
