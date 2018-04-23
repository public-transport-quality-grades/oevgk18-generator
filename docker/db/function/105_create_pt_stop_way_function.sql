CREATE OR REPLACE FUNCTION get_source(pt_stop_geom GEOMETRY) RETURNS INTEGER AS $$
   SELECT routing.source FROM routing
	      ORDER BY geom_way <-> pt_stop_geom
	      LIMIT 1;
$$ LANGUAGE sql;