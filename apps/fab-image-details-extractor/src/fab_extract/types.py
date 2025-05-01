from enum import IntEnum
from typing import TypedDict


class BoundingBox(TypedDict):
    x1: float
    y1: float
    x2: float
    y2: float


class TextExtractor(IntEnum):
    INTEGER = 1
    TITLE = 2
    LONG_TITLE = 3
    TEXTBOX = 4
    PITCH = 5


class CardType(IntEnum):
    HERO = 1
    EQUIPMENT = 2
    WEAPON = 3
    ACTION = 4
    ATTACK_REACTION = 5
    DEFENSE_REACTION = 6
    INSTANT = 7


class CardSegmentType(IntEnum):
    TYPE = 1
    TITLE = 2
    LONG_TITLE = 3
    PITCH = 4
    COST = 5
    ATTACK = 6
    DEFENSE = 7
    TEXTBOX = 8


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
