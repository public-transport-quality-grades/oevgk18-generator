from datetime import datetime
from ..context import generator


def test_calculate_transport_stop_interval():
    departures = [datetime(2018, 4, 23, 9, 1), datetime(2018, 4, 23, 9, 2), datetime(2018, 4, 23, 10, 1),
                  datetime(2018, 4, 23, 10, 2), datetime(2018, 4, 23, 11, 0), datetime(2018, 4, 23, 11, 5)]

    start_time = datetime(2018, 4, 23, 9, 0)
    end_time = datetime(2018, 4, 23, 11, 0)

    expected_interval = 3481.5

    result = generator.business.transport_stop_interval_retriever._calculate_transport_stop_interval(
        departures, start_time, end_time)

    assert result == expected_interval