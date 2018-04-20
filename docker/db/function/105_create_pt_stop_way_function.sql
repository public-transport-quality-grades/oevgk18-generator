CREATE OR REPLACE FUNCTION min_distance(pt_stop GEOMETRY) RETURNS INTEGER AS $$
    SELECT routing.source FROM routing
        ORDER BY ST_StartPoint(routing.geom_way) <-> ST_SetSRID(pt_stop, 4326)
        LIMIT 1
$$ LANGUAGE sql;