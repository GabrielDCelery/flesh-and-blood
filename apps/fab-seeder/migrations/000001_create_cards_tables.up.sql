BEGIN;

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
	FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE CASCADE,
	UNIQUE (card_id, segment_type)
);

COMMIT;
