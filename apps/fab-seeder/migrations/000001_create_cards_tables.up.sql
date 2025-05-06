BEGIN;

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE TYPE card_type AS ENUM (
	'hero',
	'equipment',
	'weapon',
	'action',
	'attack_reaction',
	'defense_reaction',
	'instant'
);

CREATE TYPE segment_type AS ENUM (
	'type',
	'title',
	'long_title',
	'pitch',
	'cost',
	'attack',
	'defense',
	'textbox'
);

CREATE TABLE IF NOT EXISTS cards (
	card_id serial PRIMARY KEY,
	card_name VARCHAR(10),
	card_type card_type,
	UNIQUE (card_name)
);

CREATE TABLE IF NOT EXISTS card_segments (
	card_id INT,
	segment_type segment_type,
	text TEXT,
	-- search TSVECTOR GENERATED ALWAYS AS (to_tsvector('english',text)) STORED,
	FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE CASCADE,
	UNIQUE (card_id, segment_type)
);

CREATE MATERIALIZED VIEW card_details AS
SELECT 
    c.card_id,
    c.card_name,
    c.card_type,
    MAX(CASE WHEN cs.segment_type = 'type' THEN cs.text END) as type,
    MAX(CASE WHEN cs.segment_type = 'title' THEN cs.text END) as title,
    MAX(CASE WHEN cs.segment_type = 'long_title' THEN cs.text END) as long_title,
    MAX(CASE WHEN cs.segment_type = 'pitch' THEN cs.text END) as pitch,
    MAX(CASE WHEN cs.segment_type = 'cost' THEN cs.text END) as cost,
    MAX(CASE WHEN cs.segment_type = 'attack' THEN cs.text END) as attack,
    MAX(CASE WHEN cs.segment_type = 'defense' THEN cs.text END) as defense,
    MAX(CASE WHEN cs.segment_type = 'textbox' THEN cs.text END) as textbox,
    setweight(to_tsvector('english', COALESCE(MAX(CASE WHEN cs.segment_type = 'title' THEN cs.text END), '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(MAX(CASE WHEN cs.segment_type = 'long_title' THEN cs.text END), '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(MAX(CASE WHEN cs.segment_type = 'type' THEN cs.text END), '')), 'B') ||
    setweight(to_tsvector('english', COALESCE(MAX(CASE WHEN cs.segment_type = 'textbox' THEN cs.text END), '')), 'C') as search_vector
FROM cards c
LEFT JOIN card_segments cs ON c.card_id = cs.card_id
GROUP BY c.card_id, c.card_name, c.card_type;

CREATE INDEX search_vector_idx ON card_details USING gin(search_vector);

COMMIT;
