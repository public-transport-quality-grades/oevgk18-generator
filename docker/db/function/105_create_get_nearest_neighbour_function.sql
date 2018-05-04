CREATE OR REPLACE FUNCTION get_source(stop_geom GEOMETRY) RETURNS INTEGER AS $$
   SELECT id FROM vertex
	      ORDER BY geom_vertex <#> stop_geom
	      LIMIT 1;
$$ LANGUAGE sql;