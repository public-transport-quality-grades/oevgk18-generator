CREATE OR REPLACE FUNCTION get_height(geom GEOMETRY)
  RETURNS TABLE(height DOUBLE PRECISION) AS $$

SELECT ST_Value(ST_SetSRID(rast, 2056), 1, geom) AS height
FROM swissalti3d
WHERE ST_intersects(rast, geom);

$$
LANGUAGE sql;