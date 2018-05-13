import pytest

from .mock import mock_gradings
from generator.output import geojson_writer
from .expected_geojson_output import write_gradings_1


def test_write_gradings(monkeypatch):
    monkeypatch.setattr(geojson_writer, '_write_geojson',
                        lambda output_dir, due_date_config, feature_collection:
                        _assert_geojson_output(write_gradings_1.result, feature_collection))

    gradings = mock_gradings.mock_gradings()

    geojson_writer.write_gradings(mock_gradings.mock_output_config(), mock_gradings.mock_due_date_config(), gradings)


def _assert_geojson_output(expected_geojson_result: dict, feature_collection: dict):
    assert expected_geojson_result == feature_collection
