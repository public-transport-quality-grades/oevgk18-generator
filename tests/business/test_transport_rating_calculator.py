import pytest

from ..context import generator
from generator.business.util.public_transport_group import PublicTransportGroup
from generator.business.model.transport_stop import TransportStop
from .mock import mock_timetable_service


@pytest.mark.parametrize("transport_stop, expected", [
    (TransportStop('', 8503400, None, []), PublicTransportGroup.A),
    (TransportStop('', 8503125, None, []), PublicTransportGroup.B),
    (TransportStop('', 8591382, None, []), PublicTransportGroup.C),
])
def test_calculate_transport_group(transport_stop, expected):
    transport_rating = generator.business.transport_stop_rating_calculator.calculate_transport_group(
        _mock_registry(), transport_stop)
    assert transport_rating == expected


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