CREATE OR REPLACE FUNCTION transform_to_2056(geom geometry) RETURNS geometry AS $$
    SELECT ST_Transform(ST_SetSRID($1, 4326), 2056);
$$ LANGUAGE sql;