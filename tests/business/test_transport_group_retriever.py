import pytest

from ..context import generator
from generator.business.util.public_transport_group import PublicTransportGroup
from .mock import mock_timetable_service, mock_transport_stop_service, mock_registry


def test_calculate_transport_groups():
    expected_transport_groups = {
        8503400: PublicTransportGroup.A,
        8503125: PublicTransportGroup.B,
        8591382: PublicTransportGroup.C,
        8593245: PublicTransportGroup.A
    }

    registry = mock_registry.get_registry(mock_timetable_service, mock_transport_stop_service)
    transport_groups = generator.business.transport_group_retriever.calculate_transport_groups(registry)
    assert transport_groups == expected_transport_groups
