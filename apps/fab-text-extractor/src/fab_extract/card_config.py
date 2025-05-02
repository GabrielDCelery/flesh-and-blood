from fab_extract.types import (
    CardConfig,
    CardSegmentConfig,
    CardSegmentType,
    CardType,
    TextExtractor,
)

CARD_SEGMENT_TYPE: CardSegmentConfig = {
    "card_segment_type": CardSegmentType.TYPE,
    "text_extractor": TextExtractor.TITLE,
    "bounding_box": {
        "x1": 110 / 450,
        "y1": 560 / 628,
        "x2": 340 / 450,
        "y2": 590 / 628,
    },
}

CARD_SEGMENT_TITLE: CardSegmentConfig = {
    "card_segment_type": CardSegmentType.TITLE,
    "text_extractor": TextExtractor.TITLE,
    "bounding_box": {
        "x1": 85 / 450,
        "y1": 35 / 628,
        "x2": 365 / 450,
        "y2": 70 / 628,
    },
}

CARD_SEGMENT_LONG_TITLE: CardSegmentConfig = {
    "card_segment_type": CardSegmentType.LONG_TITLE,
    "text_extractor": TextExtractor.TITLE,
    "bounding_box": {
        "x1": 50 / 450,
        "y1": 35 / 628,
        "x2": 400 / 450,
        "y2": 70 / 628,
    },
}

CARD_SEGMENT_PITCH: CardSegmentConfig = {
    "card_segment_type": CardSegmentType.PITCH,
    "text_extractor": TextExtractor.PITCH,
    "bounding_box": {
        "x1": 30 / 450,
        "y1": 30 / 628,
        "x2": 75 / 450,
        "y2": 75 / 628,
    },
}

CARD_SEGMENT_COST: CardSegmentConfig = {
    "card_segment_type": CardSegmentType.COST,
    "text_extractor": TextExtractor.INTEGER,
    "bounding_box": {
        "x1": 385 / 450,
        "y1": 45 / 628,
        "x2": 405 / 450,
        "y2": 70 / 628,
    },
}


CARD_SEGMENT_ATTACK: CardSegmentConfig = {
    "card_segment_type": CardSegmentType.ATTACK,
    "text_extractor": TextExtractor.INTEGER,
    "bounding_box": {
        "x1": 70 / 450,
        "y1": 570 / 628,
        "x2": 100 / 450,
        "y2": 600 / 628,
    },
}

CARD_SEGMENT_DEFENSE: CardSegmentConfig = {
    "card_segment_type": CardSegmentType.DEFENSE,
    "text_extractor": TextExtractor.INTEGER,
    "bounding_box": {
        "x1": 350 / 450,
        "y1": 570 / 628,
        "x2": 380 / 450,
        "y2": 600 / 628,
    },
}

CARD_SEGMENT_TEXTBOX: CardSegmentConfig = {
    "card_segment_type": CardSegmentType.TEXTBOX,
    "text_extractor": TextExtractor.TEXTBOX,
    "bounding_box": {
        "x1": 45 / 450,
        "y1": 400 / 628,
        "x2": 405 / 450,
        "y2": 550 / 628,
    },
}

CARD_CONFIG_HERO: CardConfig = {
    "card_type": CardType.HERO,
    "wording": "hero",
    "segments": [
        CARD_SEGMENT_TYPE,
        CARD_SEGMENT_LONG_TITLE,
        CARD_SEGMENT_TEXTBOX,
        CARD_SEGMENT_ATTACK,
        CARD_SEGMENT_DEFENSE,
    ],
}

CARD_CONFIG_EQUIPMENT: CardConfig = {
    "card_type": CardType.EQUIPMENT,
    "wording": "equipment",
    "segments": [
        CARD_SEGMENT_TYPE,
        CARD_SEGMENT_LONG_TITLE,
        CARD_SEGMENT_TEXTBOX,
        CARD_SEGMENT_DEFENSE,
    ],
}

CARD_CONFIG_WEAPON: CardConfig = {
    "card_type": CardType.WEAPON,
    "wording": "weapon",
    "segments": [
        CARD_SEGMENT_TYPE,
        CARD_SEGMENT_LONG_TITLE,
        CARD_SEGMENT_TEXTBOX,
        CARD_SEGMENT_ATTACK,
    ],
}


CARD_CONFIG_ACTION: CardConfig = {
    "card_type": CardType.ACTION,
    "wording": "action",
    "segments": [
        CARD_SEGMENT_TYPE,
        CARD_SEGMENT_TITLE,
        CARD_SEGMENT_PITCH,
        CARD_SEGMENT_COST,
        CARD_SEGMENT_TEXTBOX,
        CARD_SEGMENT_ATTACK,
        CARD_SEGMENT_DEFENSE,
    ],
}

CARD_CONFIG_ATTACK_REACTION: CardConfig = {
    "card_type": CardType.ATTACK_REACTION,
    "wording": "attack reaction",
    "segments": [
        CARD_SEGMENT_TYPE,
        CARD_SEGMENT_TITLE,
        CARD_SEGMENT_PITCH,
        CARD_SEGMENT_COST,
        CARD_SEGMENT_TEXTBOX,
        CARD_SEGMENT_DEFENSE,
    ],
}

CARD_CONFIG_DEFENSE_REACTION: CardConfig = {
    "card_type": CardType.DEFENSE_REACTION,
    "wording": "defense reaction",
    "segments": [
        CARD_SEGMENT_TYPE,
        CARD_SEGMENT_TITLE,
        CARD_SEGMENT_PITCH,
        CARD_SEGMENT_COST,
        CARD_SEGMENT_TEXTBOX,
        CARD_SEGMENT_DEFENSE,
    ],
}

CARD_CONFIG_INSTANT: CardConfig = {
    "card_type": CardType.INSTANT,
    "wording": "instant",
    "segments": [
        CARD_SEGMENT_TYPE,
        CARD_SEGMENT_TITLE,
        CARD_SEGMENT_PITCH,
        CARD_SEGMENT_COST,
        CARD_SEGMENT_TEXTBOX,
    ],
}

CARD_CONFIGS: list[CardConfig] = [
    CARD_CONFIG_HERO,
    CARD_CONFIG_EQUIPMENT,
    CARD_CONFIG_WEAPON,
    CARD_CONFIG_ACTION,
    CARD_CONFIG_ATTACK_REACTION,
    CARD_CONFIG_DEFENSE_REACTION,
    CARD_CONFIG_INSTANT,
]
