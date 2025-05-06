BEGIN;

DROP VIEW [IF EXISTS] view_name;
DROP TABLE card_segments;
DROP TABLE cards;
DROP TYPE segment_type;
DROP TYPE card_type;

COMMIT;
