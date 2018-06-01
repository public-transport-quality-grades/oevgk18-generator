from ..context import generator
from generator.business.model.public_transport_group import PublicTransportGroup
from .mock import mock_timetable_service, mock_transport_stop_service, mock_transport_stops, mock_registry


def test_calculate_transport_groups():
    expected_transport_groups = {
        mock_transport_stops.stop_8503400: PublicTransportGroup.A,
        mock_transport_stops.stop_8503125: PublicTransportGroup.B,
        mock_transport_stops.stop_8591382: PublicTransportGroup.C,
        mock_transport_stops.stop_8593245: PublicTransportGroup.A,
        mock_transport_stops.stop_8504532: PublicTransportGroup.A
    }

    registry = mock_registry.get_registry(mock_timetable_service, mock_transport_stop_service)
    transport_groups = generator.business.transport_group_retriever.get_transport_groups(registry)
    assert transport_groups == expected_transport_groups
