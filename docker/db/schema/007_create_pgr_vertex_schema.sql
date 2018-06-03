DROP TABLE IF EXISTS routing_segmented_vertices_pgr;

CREATE TABLE routing_segmented_vertices_pgr (
  id       BIGINT,
  cnt      INTEGER,
  chk      INTEGER,
  ein      INTEGER,
  eout     INTEGER,
  the_geom GEOMETRY(Point, 4326)
);