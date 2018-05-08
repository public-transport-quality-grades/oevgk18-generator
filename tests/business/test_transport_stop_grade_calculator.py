from ..context import generator
from generator.business.util.public_transport_stop_category import PublicTransportStopCategory
from generator.business.util.public_transport_stop_grade import PublicTransportStopGrade
from generator.business.model.grading import Grading
from .mock import mock_routing_engine_service
from .mock.mock_isochrone import fake_isochrone

TRANSPORT_STOP_RATINGS = {
        8503400: PublicTransportStopCategory.I,
        8503125: PublicTransportStopCategory.II,
        8591382: PublicTransportStopCategory.III,
        8593245: None
}


def test_calculate_transport_stop_grades():
    expected_gradings = {
        8503400: [Grading(fake_isochrone(450.0), PublicTransportStopGrade.A),
                  Grading(fake_isochrone(1350.0), PublicTransportStopGrade.F)],
        8503125:  [Grading(fake_isochrone(450.0), PublicTransportStopGrade.B),
                   Grading(fake_isochrone(900.0), PublicTransportStopGrade.E)],
        8591382: [Grading(fake_isochrone(450.0), PublicTransportStopGrade.C)],
    }

    gradings = generator.business.transport_stop_grade_calculator.calculate_transport_stop_grades(
        _mock_registry(), TRANSPORT_STOP_RATINGS)

    assert gradings == expected_gradings


def _mock_registry():
    return {
        'routing_engine_service': mock_routing_engine_service,
        'config': {
            'database-connections': {},
            'isochrones': [
                {'walking-speed': 1.5}
            ],
            "public-transport-ratings": [
                {
                    "max-seconds": 300,
                    "transport-stop-categories": [
                        {
                            1: "A"
                        },
                        {
                            2: "B"
                        },
                        {
                            3: "C"
                        }
                    ]
                },
                {
                    "max-seconds": 600,
                    "transport-stop-categories": [
                        {
                            1: "D"
                        },
                        {
                            2: "E"
                        },
                    ]
                },
                {
                    "max-seconds": 900,
                    "transport-stop-categories": [
                        {
                            1: "F"
                        },
                    ]
                }
            ]
        }
    }