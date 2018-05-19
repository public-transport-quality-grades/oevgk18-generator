CREATE INDEX ON routing USING GIST (geom_way);

CREATE INDEX ON vertex USING GIST (geom_vertex);
CREATE INDEX ON vertex USING GIST(geography(geom_vertex));
