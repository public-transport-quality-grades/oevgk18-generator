from shapely import wkt

from ..context import generator


def test_round_geometry_polygon():
    polygon_wkt = "POLYGON ((9.42109 46.7626, 9.42108 46.7625, 9.421049999999999 46.76241, 9.420999999999999" \
                  " 46.76486, 9.42193 46.7645, 9.42109 46.7626))"

    polygon_expected = "POLYGON ((9.42109 46.7626, 9.42108 46.7625, 9.42105 46.76241, 9.421" \
                       " 46.76486, 9.42193 46.7645, 9.42109 46.7626))"
    polygon = wkt.loads(polygon_wkt)
    round_polygon = generator.output.util.round_geometry.round_geometry_coordinates(polygon)

    assert round_polygon == wkt.loads(polygon_expected)
