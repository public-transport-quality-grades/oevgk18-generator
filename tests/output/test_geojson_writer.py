import pytest

from .mock import mock_config, mock_gradings, mock_transport_stops
from generator.output import geojson_writer
from .expected_geojson_output import nonintercepting, intercepting_same_grade, same_uic_ref_overlapping
from .expected_geojson_output import different_uic_ref_overlapping, different_uic_ref_and_grades
from .expected_geojson_output import transport_stops


def test_write_gradings_noninterception(monkeypatch):
    monkeypatch.setattr(geojson_writer, '_write_geojson',
                        lambda output_dir, filename, feature_collection:
                        _assert_geojson_output(nonintercepting.result, feature_collection))

    gradings = mock_gradings.mock_gradings_non_intercepting()

    geojson_writer.write_gradings(mock_config.mock_output_config(), mock_config.mock_due_date_config(), gradings)


def test_write_gradings_intercepting_same_grade(monkeypatch):
    monkeypatch.setattr(geojson_writer, '_write_geojson',
                        lambda output_dir, filename, feature_collection:
                        _assert_geojson_output(intercepting_same_grade.result, feature_collection))

    gradings = mock_gradings.mock_gradings_intercepting_same_grade()

    geojson_writer.write_gradings(mock_config.mock_output_config(), mock_config.mock_due_date_config(), gradings)


def test_write_gradings_same_uic_ref_overlapping(monkeypatch):
    monkeypatch.setattr(geojson_writer, '_write_geojson',
                        lambda output_dir, filename, feature_collection:
                        _assert_geojson_output(same_uic_ref_overlapping.result, feature_collection))

    gradings = mock_gradings.mock_gradings_same_uic_ref_overlapping()

    geojson_writer.write_gradings(mock_config.mock_output_config(), mock_config.mock_due_date_config(), gradings)


def test_write_gradings_different_uic_ref_overlapping(monkeypatch):
    monkeypatch.setattr(geojson_writer, '_write_geojson',
                        lambda output_dir, filename, feature_collection:
                        _assert_geojson_output(different_uic_ref_overlapping.result, feature_collection))

    gradings = mock_gradings.mock_gradings_different_uic_ref_overlapping()

    geojson_writer.write_gradings(mock_config.mock_output_config(), mock_config.mock_due_date_config(), gradings)


def test_write_gradings_different_uic_ref_and_grades(monkeypatch):
    monkeypatch.setattr(geojson_writer, '_write_geojson',
                        lambda output_dir, filename, feature_collection:
                        _assert_geojson_output(different_uic_ref_and_grades.result, feature_collection))

    gradings = mock_gradings.mock_gradings_different_uic_ref_and_grades()

    geojson_writer.write_gradings(mock_config.mock_output_config(), mock_config.mock_due_date_config(), gradings)


def test_write_transport_stops(monkeypatch):
    monkeypatch.setattr(geojson_writer, '_write_geojson',
                        lambda output_dir, filename, feature_collection:
                        _assert_geojson_output(transport_stops.result, feature_collection))

    transport_stop_list = mock_transport_stops.mock_transport_stops()
    geojson_writer.write_transport_stops(mock_config.mock_output_config(), transport_stop_list)


def _assert_geojson_output(expected_geojson_result: dict, feature_collection: dict):
    assert expected_geojson_result == feature_collection
