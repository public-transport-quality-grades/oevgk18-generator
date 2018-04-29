import pytest

from ..context import generator
from generator.business.util.public_transport_group import PublicTransportGroup
from generator.business.util.public_transport_stop_category import PublicTransportStopCategory
from generator.business.model.transport_stop import TransportStop
from .mock import mock_timetable_service

TRANSPORT_STOPS = [
    TransportStop('', 8503400, None, []),
    TransportStop('', 8503125, None, []),
    TransportStop('', 8591382, None, []),
    TransportStop('', 8593245, None, []),
]


def test_calculate_transport_group():

    expected_transport_groups = {
        8503400: PublicTransportGroup.A,
        8503125: PublicTransportGroup.B,
        8591382: PublicTransportGroup.C,
        8593245: PublicTransportGroup.A
    }

    transport_ratings = generator.business.transport_stop_rating_calculator.calculate_transport_groups(
        _mock_registry(), TRANSPORT_STOPS)
    assert transport_ratings == expected_transport_groups


def test_calculate_transport_stop_categories():
    transport_groups = {
        8503400: PublicTransportGroup.A,
        8503125: PublicTransportGroup.B,
        8591382: PublicTransportGroup.C,
        8593245: PublicTransportGroup.A,
    }

    intervals = {
        8503400: 200.34,
        8503125: 2400,
        8591382: None,
        8593245: 10000.63
    }

    expected_stop_categories = {
        8503400: PublicTransportStopCategory.I,
        8503125: PublicTransportStopCategory.IV,
        8591382: PublicTransportStopCategory.VII,
        8593245: None
    }

    stop_categories = generator.business.transport_stop_rating_calculator.calculate_transport_stop_categories(
        _mock_registry(), TRANSPORT_STOPS, transport_groups, intervals)

    assert len(stop_categories) == len(expected_stop_categories)
    assert stop_categories == expected_stop_categories


def _mock_registry():
    return {
        'timetable_service': mock_timetable_service,
        'config': {
            'database-connections': {},
            'public-transport-types': {
                'train-junction-min-directions': 6
            },
            "transport-stop-categories": [
                {
                    "max-interval": 300,
                    "transport-type-mappings": [
                        {
                            "A": 1
                        },
                        {
                            "B": 1
                        },
                        {
                            "C": 2
                        }
                    ]
                },
                {
                    "min-interval": 1200,
                    "max-interval": 2400,
                    "transport-type-mappings": [
                        {
                            "A": 3
                        },
                        {
                            "B": 4
                        },
                        {
                            "C": 5
                        }
                    ]
                },
                {
                    "min-interval": 2400,
                    "transport-type-mappings": [
                        {
                            "B": 7
                        },
                        {
                            "C": 7
                        }
                    ]
                }
            ]
        }
    }