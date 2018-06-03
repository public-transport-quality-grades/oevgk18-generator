DROP TABLE IF EXISTS stop_vertex_mapping;

CREATE TABLE stop_vertex_mapping (
  id                SERIAL  NOT NULL PRIMARY KEY,
  stop_uic_ref      BIGINT  NOT NULL,
  nearest_vertex_id INTEGER NOT NULL
);