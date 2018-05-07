from datetime import datetime
from ..context import generator
from .mock import mock_timetable_service, mock_registry


def test_calculate_transport_stop_interval_trivial():
    """example from the VISUM 12 book"""
    registry = mock_registry.get_registry(mock_timetable_service)

    stops = [
        8503400
    ]

    due_date_config = {
        'due-date': datetime(2018, 4, 23),
        'lower-bound': '06:00',
        'upper-bound': '07:00'
    }

    expected_interval = {
        8503400: 2600
    }

    result = generator.business.transport_stop_interval_retriever.get_transport_stop_intervals(
        registry, due_date_config, stops)

    assert result == expected_interval


def test_calculate_transport_stop_interval_regular():
    # with more data, the algorithm gets closer to the "real" interval
    registry = mock_registry.get_registry(mock_timetable_service)

    stops = [
        8503125
    ]

    due_date_config = {
        'due-date': datetime(2018, 4, 23),
        'lower-bound': '08:40',
        'upper-bound': '16:40'
    }

    expected_interval = {
        8503125: 890.625  # 14 min 50s
    }

    result = generator.business.transport_stop_interval_retriever.get_transport_stop_intervals(
        registry, due_date_config, stops)

    assert result == expected_interval


def test_calculate_transport_stop_interval_skewed():
    registry = mock_registry.get_registry(mock_timetable_service)

    stops = [
        8591382
    ]

    due_date_config = {
        'due-date': datetime(2018, 4, 23),
        'lower-bound': '09:00',
        'upper-bound': '11:00'
    }

    expected_interval = {
        8591382: 3481.5  # 58.01 min
    }

    result = generator.business.transport_stop_interval_retriever.get_transport_stop_intervals(
        registry, due_date_config, stops)

    assert result == expected_interval
