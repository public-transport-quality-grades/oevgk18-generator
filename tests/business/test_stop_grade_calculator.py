from generator.business.model.grading import Grading
from generator.business.model.stop_category import StopCategory
from generator.business.model.stop_grade import StopGrade
from .mock import mock_registry
from .mock import mock_routing_engine_service
from .mock.mock_isochrone import fake_isochrone
from ..context import generator

TRANSPORT_STOP_RATINGS = {
    8503400: StopCategory.I,
    8503125: StopCategory.II,
    8591382: StopCategory.III,
    8593245: None
}


def test_calculate_stop_grades():
    expected_gradings = {
        8503400: [Grading(fake_isochrone(450.0), StopGrade.A),
                  Grading(fake_isochrone(1350.0), StopGrade.F)],
        8503125: [Grading(fake_isochrone(450.0), StopGrade.B),
                  Grading(fake_isochrone(900.0), StopGrade.E)],
        8591382: [Grading(fake_isochrone(450.0), StopGrade.C)],
    }

    gradings = generator.business.stop_grade_calculator.calculate_stop_grades(
        mock_registry.get_registry(routing_engine_service=mock_routing_engine_service), TRANSPORT_STOP_RATINGS)

    assert gradings == expected_gradings
