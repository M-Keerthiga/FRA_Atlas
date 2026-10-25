CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE IF NOT EXISTS states (
  id BIGSERIAL PRIMARY KEY, code TEXT UNIQUE, name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS districts (
  id BIGSERIAL PRIMARY KEY, state_id BIGINT NOT NULL REFERENCES states(id), code TEXT,
  name TEXT NOT NULL, boundary geometry(MultiPolygon, 4326), UNIQUE(state_id, name)
);
CREATE TABLE IF NOT EXISTS blocks (
  id BIGSERIAL PRIMARY KEY, district_id BIGINT NOT NULL REFERENCES districts(id),
  name TEXT NOT NULL, boundary geometry(MultiPolygon, 4326), UNIQUE(district_id, name)
);
CREATE TABLE IF NOT EXISTS villages (
  id BIGSERIAL PRIMARY KEY, block_id BIGINT NOT NULL REFERENCES blocks(id),
  name TEXT NOT NULL, population BIGINT, households BIGINT,
  boundary geometry(MultiPolygon, 4326), UNIQUE(block_id, name)
);
CREATE TABLE IF NOT EXISTS data_sources (
  id BIGSERIAL PRIMARY KEY, title TEXT NOT NULL, publisher TEXT, source_url TEXT,
  publication_date DATE, reporting_period TEXT, downloaded_at TIMESTAMPTZ DEFAULT now(),
  notes TEXT, verified BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS fra_statistics (
  id BIGSERIAL PRIMARY KEY, state_id BIGINT REFERENCES states(id), district_id BIGINT REFERENCES districts(id),
  block_id BIGINT REFERENCES blocks(id), village_id BIGINT REFERENCES villages(id),
  report_date DATE, claims_received BIGINT, claims_approved BIGINT, claims_pending BIGINT,
  claims_rejected BIGINT, ifr_claims BIGINT, cr_claims BIGINT, cfr_claims BIGINT,
  forest_area_ha NUMERIC, agricultural_land_ha NUMERIC, source_id BIGINT REFERENCES data_sources(id),
  source_row_reference TEXT, imported_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (claims_received IS NULL OR claims_received >= 0),
  CHECK (claims_approved IS NULL OR claims_approved >= 0),
  CHECK (claims_pending IS NULL OR claims_pending >= 0),
  CHECK (claims_rejected IS NULL OR claims_rejected >= 0)
);
CREATE INDEX IF NOT EXISTS idx_districts_boundary ON districts USING GIST(boundary);
CREATE INDEX IF NOT EXISTS idx_blocks_boundary ON blocks USING GIST(boundary);
CREATE INDEX IF NOT EXISTS idx_villages_boundary ON villages USING GIST(boundary);
CREATE INDEX IF NOT EXISTS idx_fra_statistics_report_date ON fra_statistics(report_date);
CREATE INDEX IF NOT EXISTS idx_fra_statistics_geo ON fra_statistics(state_id, district_id, block_id, village_id);
-- Deliberately no INSERT statements: load only verified official source data.
