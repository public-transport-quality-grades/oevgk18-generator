CREATE OR REPLACE FUNCTION get_height(geom GEOMETRY) RETURNS TABLE(height double precision) AS $$
    SELECT ST_Value(ST_SetSRID(sub.rast, 2056), 1, $1) AS height FROM
      (SELECT rid, rast FROM swissalti3d WHERE ST_Intersects(ST_SetSRID(rast, 2056), $1)) AS sub;
$$ LANGUAGE sql;