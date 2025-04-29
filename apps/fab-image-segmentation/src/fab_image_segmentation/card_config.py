from typing import TypedDict


class BoundingBox(TypedDict):
    x1: float
    y1: float
    x2: float
    y2: float


class CardRegionConfig(TypedDict):
    name: str
    bounding_box: BoundingBox


class CardConfig(TypedDict):
    regions: list[CardRegionConfig]


fab_card_config: CardConfig = {
    "regions": [
        {
            "name": "pitch",
            "bounding_box": {
                "x1": 30 / 450,
                "y1": 30 / 628,
                "x2": 75 / 450,
                "y2": 75 / 628,
            },
        },
        {
            "name": "widetitle",
            "bounding_box": {
                "x1": 50 / 450,
                "y1": 35 / 628,
                "x2": 400 / 450,
                "y2": 70 / 628,
            },
        },
        {
            "name": "title",
            "bounding_box": {
                "x1": 85 / 450,
                "y1": 35 / 628,
                "x2": 365 / 450,
                "y2": 70 / 628,
            },
        },
        {
            "name": "cost",
            "bounding_box": {
                "x1": 385 / 450,
                "y1": 45 / 628,
                "x2": 405 / 450,
                "y2": 70 / 628,
            },
        },
        {
            "name": "power",
            "bounding_box": {
                "x1": 70 / 450,
                "y1": 570 / 628,
                "x2": 100 / 450,
                "y2": 600 / 628,
            },
        },
        {
            "name": "defense",
            "bounding_box": {
                "x1": 350 / 450,
                "y1": 570 / 628,
                "x2": 380 / 450,
                "y2": 600 / 628,
            },
        },
        {
            "name": "textbox",
            "bounding_box": {
                "x1": 45 / 450,
                "y1": 400 / 628,
                "x2": 405 / 450,
                "y2": 550 / 628,
            },
        },
        {
            "name": "type",
            "bounding_box": {
                "x1": 110 / 450,
                "y1": 560 / 628,
                "x2": 340 / 450,
                "y2": 590 / 628,
            },
        },
    ]
}
