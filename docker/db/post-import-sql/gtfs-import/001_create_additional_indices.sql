CREATE INDEX ON stops(stop_id);
CREATE INDEX ON stop_times(stop_id);
CREATE INDEX ON stop_times(trip_id);
CREATE INDEX ON trips(trip_id);
CREATE INDEX ON trips(route_id);
CREATE INDEX ON routes(route_id);
CREATE INDEX ON calendar_dates(service_id);