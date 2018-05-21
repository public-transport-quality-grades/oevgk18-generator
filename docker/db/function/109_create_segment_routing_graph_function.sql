CREATE OR REPLACE FUNCTION segment_routing_graph(segment_size_m INTEGER) RETURNS VOID AS $$
BEGIN
 TRUNCATE routing_segmented;
 INSERT INTO routing_segmented(geom_way, osm_id)
   SELECT segs.geom, routing.osm_id
   FROM routing
   CROSS JOIN segments(routing.geom_way, routing.km * 1000, segment_size_m) AS segs
   WHERE routing.relevant IS TRUE AND routing.km != 0;

 DROP TABLE IF EXISTS routing_segmented_vertices_pgr;
 PERFORM pgr_createTopology('routing_segmented', 0.00001, 'geom_way', 'id');

 UPDATE routing_segmented
   SET cost = ST_LengthSpheroid(geom_way, 'SPHEROID["WGS84",6378137,298.25728]');

END;
$$ LANGUAGE plpgsql;
