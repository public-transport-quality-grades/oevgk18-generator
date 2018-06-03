ALTER TABLE stops
  ADD COLUMN uic_ref INTEGER NULL;

UPDATE stops
SET uic_ref = split_part(stop_id, ':', 1) :: integer;