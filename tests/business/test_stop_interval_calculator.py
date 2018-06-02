from datetime import datetime
from ..context import generator
from .mock import mock_timetable_service, mock_registry, mock_transport_stops


def test_calculate_stop_intervals_trivial():
    """example from the VISUM 12 book"""
    registry = mock_registry.get_registry(mock_timetable_service)

    stops = [
        mock_transport_stops.stop_8503400
    ]

    due_date_config = {
        'due-date': datetime(2018, 4, 23),
        'lower-bound': '06:00',
        'upper-bound': '07:00'
    }

    expected_interval = {
        mock_transport_stops.stop_8503400.uic_ref: 2600
    }

    result = generator.business.stop_interval_calculator.calculate_stop_intervals(
        registry, due_date_config, stops)

    assert result == expected_interval


def test_calculate_stop_intervals_regular():
    # with more data, the algorithm gets closer to the "real" interval
    registry = mock_registry.get_registry(mock_timetable_service)

    stops = [
        mock_transport_stops.stop_8503125
    ]

    due_date_config = {
        'due-date': datetime(2018, 4, 23),
        'lower-bound': '08:40',
        'upper-bound': '16:40'
    }

    expected_interval = {
        mock_transport_stops.stop_8503125.uic_ref: 890.625  # 14 min 50s
    }

    result = generator.business.stop_interval_calculator.calculate_stop_intervals(
        registry, due_date_config, stops)

    assert result == expected_interval


def test_calculate_stop_intervals_skewed():
    registry = mock_registry.get_registry(mock_timetable_service)

    stops = [
        mock_transport_stops.stop_8591382
    ]

    due_date_config = {
        'due-date': datetime(2018, 4, 23),
        'lower-bound': '09:00',
        'upper-bound': '11:00'
    }

    expected_interval = {
        mock_transport_stops.stop_8591382.uic_ref: 3481.5  # 58.01 min
    }

    result = generator.business.stop_interval_calculator.calculate_stop_intervals(
        registry, due_date_config, stops)

    assert result == expected_interval
