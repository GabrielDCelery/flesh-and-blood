from enum import IntEnum
from typing import TypedDict


class BoundingBox(TypedDict):
    x1: float
    y1: float
    x2: float
    y2: float


class TextExtractor(IntEnum):
    INTEGER = 0
    TITLE = 1
    LONG_TITLE = 2
    TEXTBOX = 3
    PITCH = 4


class CardType(IntEnum):
    HERO = 0
    EQUIPMENT = 1
    WEAPON = 2
    ACTION = 3
    ATTACK_REACTION = 4
    DEFENSE_REACTION = 5
    INSTANT = 6


class CardSegmentType(IntEnum):
    TYPE = 0
    TITLE = 1
    LONG_TITLE = 2
    PITCH = 3
    COST = 4
    ATTACK = 5
    DEFENSE = 6
    TEXTBOX = 7


class CardSegmentConfig(TypedDict):
    card_segment_type: CardSegmentType
    text_extractor: TextExtractor
    bounding_box: BoundingBox


class CardConfig(TypedDict):
    card_type: CardType
    wording: str
    segments: list[CardSegmentConfig]


class CardSegmentDetails(TypedDict):
    card_segment_type: CardSegmentType
    text: str


class CardDetails(TypedDict):
    card_type: CardType
    segments: list[CardSegmentDetails]
