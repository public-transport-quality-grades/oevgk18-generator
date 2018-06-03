CREATE TABLE agency
(
  agency_id       TEXT UNIQUE NULL,
  agency_name     TEXT        NOT NULL,
  agency_url      TEXT        NOT NULL,
  agency_timezone TEXT        NOT NULL,
  agency_lang     TEXT        NULL,
  agency_phone    TEXT        NULL
);

CREATE TABLE stops
(
  stop_id              TEXT PRIMARY KEY,
  stop_code            TEXT             NULL,
  stop_name            TEXT             NOT NULL,
  stop_desc            TEXT             NULL,
  stop_lat             DOUBLE PRECISION NOT NULL,
  stop_lon             DOUBLE PRECISION NOT NULL,
  stop_elevation       INTEGER          NULL,
  zone_id              TEXT             NULL,
  stop_url             TEXT             NULL,
  location_type        BOOLEAN          NULL,
  parent_station       TEXT             NULL,
  platform_code        TEXT             NULL,
  ch_station_long_name TEXT             NULL,
  ch_station_synonym1  TEXT             NULL,
  ch_station_synonym2  TEXT             NULL,
  ch_station_synonym3  TEXT             NULL,
  ch_station_synonym4  TEXT             NULL
);

CREATE TABLE routes
(
  route_id         TEXT PRIMARY KEY,
  agency_id        TEXT    NULL REFERENCES agency (agency_id),
  route_short_name TEXT    NULL,
  route_long_name  TEXT    NULL,
  route_desc       TEXT    NULL,
  route_type       INTEGER NULL,
  route_url        TEXT    NULL,
  route_color      TEXT    NULL,
  route_text_color TEXT    NULL
);

CREATE TABLE calendar
(
  service_id TEXT PRIMARY KEY,
  monday     BOOLEAN    NOT NULL,
  tuesday    BOOLEAN    NOT NULL,
  wednesday  BOOLEAN    NOT NULL,
  thursday   BOOLEAN    NOT NULL,
  friday     BOOLEAN    NOT NULL,
  saturday   BOOLEAN    NOT NULL,
  sunday     BOOLEAN    NOT NULL,
  start_date NUMERIC(8) NOT NULL,
  end_date   NUMERIC(8) NOT NULL
);

CREATE TABLE calendar_dates
(
  service_id     TEXT       NOT NULL,
  date           NUMERIC(8) NOT NULL,
  exception_type INTEGER    NOT NULL
);


CREATE TABLE trips
(
  route_id        TEXT    NOT NULL REFERENCES routes (route_id),
  service_id      TEXT    NOT NULL,
  trip_id         TEXT    NOT NULL PRIMARY KEY,
  trip_headsign   TEXT    NULL,
  trip_short_name TEXT    NULL,
  direction_id    BOOLEAN NULL,
  block_id        TEXT    NULL,
  shape_id        TEXT    NULL,
  bikes_allowed   INTEGER NULL,
  attributes_ch   TEXT    NULL
);

CREATE TABLE stop_times
(
  trip_id             TEXT     NOT NULL REFERENCES trips (trip_id),
  arrival_time        INTERVAL NULL, -- should be not null according to spec
  departure_time      INTERVAL NULL, -- should be not null according to spec
  stop_id             TEXT     NOT NULL REFERENCES stops (stop_id),
  stop_sequence       INTEGER  NOT NULL,
  stop_headsign       TEXT     NULL,
  pickup_type         INTEGER  NULL CHECK (pickup_type >= 0 AND pickup_type <= 3),
  drop_off_type       INTEGER  NULL CHECK (drop_off_type >= 0 AND drop_off_type <= 3),
  shape_dist_traveled INTEGER  NULL,
  attributes_ch       TEXT     NULL
);

CREATE TABLE transfers
(
  from_stop_id      TEXT    NOT NULL REFERENCES stops (stop_id),
  to_stop_id        TEXT    NOT NULL REFERENCES stops (stop_id),
  transfer_type     INTEGER NOT NULL,
  min_transfer_time INTEGER
);

CREATE TABLE frequencies
(
  trip_id      TEXT     NOT NULL REFERENCES trips (trip_id),
  start_time   INTERVAL NOT NULL,
  end_time     INTERVAL NOT NULL,
  headway_secs INTEGER  NOT NULL
);