DROP TABLE IF EXISTS calendar_trip_mapping;
CREATE TABLE calendar_trip_mapping (
    departure_time INTERVAL,
    stop_id TEXT
);

CREATE INDEX ON calendar_trip_mapping USING gin (stop_id gin_trgm_ops);
CREATE INDEX ON calendar_trip_mapping(departure_time);