-- routing table will be overridden with a different schema during the import
ALTER TABLE routing
  ADD COLUMN IF NOT EXISTS relevant bool;
ALTER TABLE routing
  ADD COLUMN IF NOT EXISTS cost_effective DOUBLE PRECISION;