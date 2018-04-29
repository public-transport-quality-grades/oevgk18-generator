from contextlib import contextmanager
from ..context import generator

fake_db_rows = [{
        'stop_id': 1,
        'stop_name': "fakeName",
        'stop_lat': 47.3458,
        'stop_lon': 8.34982,
        'platform': [None, '1', '2']
    },
    {
        'stop_id': 1,
        'stop_name': "fakeName",
        'stop_lat': 47.3458,
        'stop_lon': 8.34982,
        'platform': [None]
    }
]


def _fake_query_transport_stop_rows(db):
    return fake_db_rows


def _fake_parse_point_geometry(geom):
    return geom


@contextmanager
def _fake_db_connection(db_config):
    yield None


def test_get_transport_stop_from_uic_ref(monkeypatch):
    monkeypatch.setattr(
        generator.integration.ptstop_service, '_query_transport_stop_rows', _fake_query_transport_stop_rows)
    monkeypatch.setattr(
        generator.integration.ptstop_service, 'db_connection', _fake_db_connection)

    transport_stops = generator.integration.ptstop_service.get_transport_stops({})

    assert transport_stops[0].uic_name == fake_db_rows[0]['stop_name']
    assert transport_stops[0].uic_ref == fake_db_rows[1]['stop_id']
    assert transport_stops[0].location.x == fake_db_rows[0]['stop_lon']
    assert transport_stops[0].location.y == fake_db_rows[0]['stop_lat']
    assert transport_stops[0].platforms == fake_db_rows[0]['platform']
    assert transport_stops[1].platforms == []
