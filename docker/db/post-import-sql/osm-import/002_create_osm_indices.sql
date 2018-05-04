CREATE INDEX ON routing USING GIST (geom_way);
CREATE INDEX ON vertex USING GIST (geom_vertex);