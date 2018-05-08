import pytest

from datetime import datetime
from ..context import generator
from generator.business.util.public_transport_stop_category import PublicTransportStopCategory
from generator.business import transport_stop_interval_retriever, transport_group_retriever
from .mock import mock_timetable_service, mock_transport_group_retriever, mock_interval_retriever, mock_registry


def test_calculate_transport_stop_ratings(monkeypatch):
    registry = mock_registry.get_registry(mock_timetable_service)
    monkeypatch.setattr(transport_group_retriever, 'calculate_transport_groups',
                        lambda reg: mock_transport_group_retriever.calculate_transport_groups(reg))

    monkeypatch.setattr(transport_stop_interval_retriever, 'get_transport_stop_intervals',
                        lambda reg, due_date_conf, stops:
                        mock_interval_retriever.get_transport_stop_intervals(reg, due_date_conf, stops))

    due_date_config = {
        'due-date': datetime(2018, 4, 23),
        'lower-bound': '09:00',
        'upper-bound': '11:00'
    }
    expected_stop_categories = {
        8503400: PublicTransportStopCategory.I,
        8503125: PublicTransportStopCategory.IV,
        8591382: PublicTransportStopCategory.VII,
        8593245: None
    }

    transport_groups = mock_transport_group_retriever.calculate_transport_groups(registry)

    stop_categories = generator.business.transport_stop_rating_calculator.calculate_transport_stop_ratings(
        registry, due_date_config, transport_groups)
    assert len(stop_categories) == len(expected_stop_categories)
    assert stop_categories == expected_stop_categories
