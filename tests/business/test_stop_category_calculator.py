from datetime import datetime
from generator.business.model.stop_category import StopCategory
from generator.business import stop_interval_calculator, transport_group_retriever
from generator.business import stop_category_calculator
from .mock import mock_timetable_service, mock_transport_group_retriever, mock_interval_calculator, mock_registry


def test_calculate_transport_stop_ratings(monkeypatch):
    registry = mock_registry.get_registry(mock_timetable_service)
    monkeypatch.setattr(transport_group_retriever, 'calculate_transport_groups',
                        lambda reg: mock_transport_group_retriever.calculate_transport_groups(reg))

    monkeypatch.setattr(stop_interval_calculator, 'calculate_stop_intervals',
                        lambda reg, due_date_conf, stops:
                        mock_interval_calculator.calculate_stop_intervals(reg, due_date_conf, stops))

    due_date_config = {
        'due-date': datetime(2018, 4, 23),
        'lower-bound': '09:00',
        'upper-bound': '11:00'
    }
    expected_stop_categories = {
        8503400: StopCategory.I,
        8503125: StopCategory.IV,
        8591382: StopCategory.VII,
        8593245: None
    }

    transport_groups = mock_transport_group_retriever.calculate_transport_groups(registry)

    stop_categories = stop_category_calculator.get_stop_categories(
        registry, due_date_config, transport_groups)
    assert len(stop_categories) == len(expected_stop_categories)
    assert stop_categories == expected_stop_categories
