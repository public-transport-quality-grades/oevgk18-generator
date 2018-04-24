import pytest

from ..context import generator
from generator.business.util.public_transport_group import PublicTransportGroup
from .mock import mock_timetable_service


@pytest.mark.parametrize("uic_ref, expected", [
    ('8503400', PublicTransportGroup.A),
    ('8503125', PublicTransportGroup.B),
    ('8591382', PublicTransportGroup.C)
])
def test_calculate_transport_stop_rating(uic_ref, expected):
    transport_rating = generator.business.transport_stop_rating_calculator.calculate_transport_stop_rating(
        _mock_registry(), uic_ref)
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