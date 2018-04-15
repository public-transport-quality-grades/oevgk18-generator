from ..context import generator

fake_db_rows = [{
        'id': 1,
        'tags': {
            'uic_ref': '42',
            'uic_name': "fake uic name",
        },
        'geom': "fake geom"
    },
    {
        'id': 2,
        'tags': {
            'uic_ref': '42',
        },
        'geom': "fake geom"
    }]


def _fake_query_transport_stop_node(db, uic_ref: str):
    return fake_db_rows


def _fake_parse_point_geometry(geom):
    return geom


def test_get_transport_stop_from_uic_ref(monkeypatch):
    monkeypatch.setattr(
        generator.integration.ptstop_service, '_query_transport_stop_node', _fake_query_transport_stop_node)
    monkeypatch.setattr(
        generator.integration.geometry_parser, 'parse_point_geometry', _fake_parse_point_geometry)
    transport_stop = generator.integration.ptstop_service.get_transport_stop_from_uic_ref(None, '42')

    assert transport_stop.uic_name == fake_db_rows[0]['tags']['uic_name']
    assert transport_stop.uic_ref == fake_db_rows[1]['tags']['uic_ref']
    assert len(transport_stop.platforms) == 2
    assert all([p.node_geom == fake_db_rows[0]['geom'] for p in transport_stop.platforms])
    assert transport_stop.platforms[0].osm_id == fake_db_rows[0]['id']
    assert transport_stop.platforms[1].osm_id == fake_db_rows[1]['id']
