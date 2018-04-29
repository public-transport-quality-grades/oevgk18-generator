import pytest

from ..context import generator
from generator.business.util.public_transport_group import PublicTransportGroup
from generator.business.model.transport_stop import TransportStop
from .mock import mock_timetable_service


def test_calculate_transport_group():
    transport_stops = [
       TransportStop('', 8503400, None, []),
       TransportStop('', 8503125, None, []),
       TransportStop('', 8591382, None, []),
    ]

    expected_transport_groups = {
        transport_stops[0]: PublicTransportGroup.A,
        transport_stops[1]: PublicTransportGroup.B,
        transport_stops[2]: PublicTransportGroup.C,
    }

    transport_ratings = generator.business.transport_stop_rating_calculator.calculate_transport_groups(
        _mock_registry(), transport_stops)
    assert transport_ratings == expected_transport_groups


def _mock_registry():
    return {
        'timetable_service': mock_timetable_service,
        'config': {
            'database-connections': {},
            'public-transport-types': {
                'train-junction-min-directions': 6
            }
        }
    }