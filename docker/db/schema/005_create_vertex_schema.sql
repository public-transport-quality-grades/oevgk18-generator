DROP TABLE IF EXISTS vertex;

CREATE TABLE vertex (
  id           INTEGER NOT NULL,
  clazz        INTEGER,
  osm_id       BIGINT,
  osm_name     CHARACTER VARYING,
  ref_count    INTEGER,
  restrictions CHARACTER VARYING,
  geom_vertex  GEOMETRY(Point, 4326),
  CONSTRAINT pkey_vertex PRIMARY KEY (id)
);