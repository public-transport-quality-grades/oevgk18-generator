from datetime import datetime
from ..context import generator


def test_calculate_transport_stop_interval_trivial():
    """example from the VISUM 12 book"""

    departures = [datetime(2018, 4, 23, 6, 35), datetime(2018, 4, 23, 7, 15)]

    start_time = datetime(2018, 4, 23, 6, 0)
    end_time = datetime(2018, 4, 23, 7, 0)

    expected_interval = 2600

    result = generator.business.transport_stop_interval_retriever._calculate_transport_stop_interval(
        departures, start_time, end_time)

    assert result == expected_interval


def test_calculate_transport_stop_interval_regular():
    departures = [datetime(2018, 4, 23, 9, 0), datetime(2018, 4, 23, 9, 15), datetime(2018, 4, 23, 9, 30),
                  datetime(2018, 4, 23, 9, 45), datetime(2018, 4, 23, 10, 0), datetime(2018, 4, 23, 10, 15),
                  datetime(2018, 4, 23, 10, 30), datetime(2018, 4, 23, 10, 45), datetime(2018, 4, 23, 11, 0),
                  datetime(2018, 4, 23, 11, 15), datetime(2018, 4, 23, 11, 30), datetime(2018, 4, 23, 11, 45),
                  datetime(2018, 4, 23, 12, 0), datetime(2018, 4, 23, 12, 15), datetime(2018, 4, 23, 12, 30),
                  datetime(2018, 4, 23, 12, 45), datetime(2018, 4, 23, 13, 0), datetime(2018, 4, 23, 13, 15),
                  datetime(2018, 4, 23, 13, 30), datetime(2018, 4, 23, 13, 45), datetime(2018, 4, 23, 14, 0),
                  datetime(2018, 4, 23, 14, 15), datetime(2018, 4, 23, 14, 30), datetime(2018, 4, 23, 14, 45),
                  datetime(2018, 4, 23, 15, 0), datetime(2018, 4, 23, 15, 15), datetime(2018, 4, 23, 15, 30),
                  datetime(2018, 4, 23, 15, 45), datetime(2018, 4, 23, 16, 0), datetime(2018, 4, 23, 16, 15),
                  datetime(2018, 4, 23, 16, 30), datetime(2018, 4, 23, 16, 45)]

    # with more data, the algorithm gets closer to the "real" interval

    start_time = datetime(2018, 4, 23, 8, 40)
    end_time = datetime(2018, 4, 23, 16, 40)

    expected_interval = 890.625  # 14 min 50s

    result = generator.business.transport_stop_interval_retriever._calculate_transport_stop_interval(
        departures, start_time, end_time)

    assert result == expected_interval


def test_calculate_transport_stop_interval_skewed():
    departures = [datetime(2018, 4, 23, 9, 1), datetime(2018, 4, 23, 9, 2), datetime(2018, 4, 23, 10, 1),
                  datetime(2018, 4, 23, 10, 2), datetime(2018, 4, 23, 11, 0), datetime(2018, 4, 23, 11, 5)]

    start_time = datetime(2018, 4, 23, 9, 0)
    end_time = datetime(2018, 4, 23, 11, 0)

    expected_interval = 3481.5  # 58.01 min

    result = generator.business.transport_stop_interval_retriever._calculate_transport_stop_interval(
        departures, start_time, end_time)

    assert result == expected_interval
