from typing import Any

import cv2
import easyocr
import numpy as np
from cv2.typing import MatLike

from fab_extract import card_config
from fab_extract.card_config import CARD_SEGMENT_TYPE
from fab_extract.types import (
    BoundingBox,
    CardConfig,
    CardDetails,
    CardSegmentDetails,
    TextExtractor,
)


class CardClassifier:
    def __init__(self, models_dir: str):
        self.ocr_reader = easyocr.Reader(["en"], model_storage_directory=models_dir)

    def classify(self, image: MatLike) -> CardConfig | None:
        (x1, y1, x2, y2) = self.get_bounding_box_abs_coordinates(
            CARD_SEGMENT_TYPE["bounding_box"], image
        )
        image_segment = image[y1:y2, x1:x2]
        results = self.ocr_reader.readtext(image_segment)
        text = " ".join([result[1] for result in results])
        text = text.strip().lower()
        for cc in card_config.CARD_CONFIGS:
            if cc["wording"] in text:
                return cc
        return None

    def extract_details(self, card_path: str) -> CardDetails | None:
        image = cv2.imread(card_path)
        card_config = self.classify(image)
        if card_config is None:
            return None
        card_details: CardDetails = {
            "card_type": card_config["card_type"],
            "segments": [],
        }
        for segment in card_config["segments"]:
            (x1, y1, x2, y2) = self.get_bounding_box_abs_coordinates(
                segment["bounding_box"], image
            )

            image_segment = image[y1:y2, x1:x2]

            if (
                segment["text_extractor"] == TextExtractor.TITLE
                or segment["text_extractor"] == TextExtractor.LONG_TITLE
            ):
                image_segment = image[y1:y2, x1:x2]
                results = self.ocr_reader.readtext(image_segment)
                text = " ".join([result[1] for result in results])
                card_segment_details: CardSegmentDetails = {
                    "card_segment_type": segment["card_segment_type"],
                    "text": text,
                }
                card_details["segments"].append(card_segment_details)
                continue

            if segment["text_extractor"] == TextExtractor.INTEGER:
                image_segment = cv2.resize(
                    image_segment, (None), fx=2, fy=2, interpolation=cv2.INTER_CUBIC
                )

                gray = cv2.cvtColor(image_segment, cv2.COLOR_BGR2GRAY)

                _, thresh = cv2.threshold(
                    gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )

                results = self.ocr_reader.readtext(thresh, allowlist="0123456890")
                text = " ".join([result[1] for result in results])
                card_segment_details: CardSegmentDetails = {
                    "card_segment_type": segment["card_segment_type"],
                    "text": text,
                }
                card_details["segments"].append(card_segment_details)
                continue

            if segment["text_extractor"] == TextExtractor.TEXTBOX:
                # Special handling for textbox
                # 1. Enhance contrast
                gray = cv2.cvtColor(image_segment, cv2.COLOR_BGR2GRAY)
                # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                enhanced = clahe.apply(gray)

                # 2. Use EasyOCR with paragraph mode
                results = self.ocr_reader.readtext(
                    enhanced,
                    paragraph=True,  # Treat as a single paragraph
                    detail=0,  # Only return the text
                    width_ths=0.7,  # Width threshold for text grouping
                    add_margin=0.1,  # Add margin to help with text detection
                    mag_ratio=1.5,  # Magnification ratio
                )

                # Join the results with newlines since it's a paragraph
                text = "\n".join(results)
                card_segment_details: CardSegmentDetails = {
                    "card_segment_type": segment["card_segment_type"],
                    "text": text,
                }
                card_details["segments"].append(card_segment_details)
                continue
            if segment["text_extractor"] == TextExtractor.PITCH:
                """
                Count red dots in the pitch region.
                Returns the number of red dots found.
                """
                # Convert to HSV color space for better color detection
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                # Define range for red color in HSV
                # Red wraps around in HSV, so we need two ranges
                lower_red1 = np.array([0, 100, 100])
                upper_red1 = np.array([10, 255, 255])
                lower_red2 = np.array([160, 100, 100])
                upper_red2 = np.array([180, 255, 255])

                # Create masks for red color
                mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
                mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
                red_mask = cv2.bitwise_or(mask1, mask2)

                # Find contours in the mask
                contours, _ = cv2.findContours(
                    red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )

                # Filter contours based on area and circularity
                red_dots = 0
                for contour in contours:
                    area = cv2.contourArea(contour)
                    perimeter = cv2.arcLength(contour, True)

                    # Avoid division by zero
                    if perimeter == 0:
                        continue

                    # Circularity = 4*pi*area/(perimeter^2)
                    circularity = 4 * np.pi * area / (perimeter * perimeter)

                    # Adjust these thresholds based on your images
                    min_area = 150  # Minimum area of a dot
                    max_area = 250  # Maximum area of a dot
                    min_circularity = 0.7  # Minimum circularity (1.0 is perfect circle)

                    if min_area <= area <= max_area and circularity >= min_circularity:
                        red_dots += 1
                card_segment_details: CardSegmentDetails = {
                    "card_segment_type": segment["card_segment_type"],
                    "text": str(red_dots),
                }
                card_details["segments"].append(card_segment_details)
                continue

        return card_details

    def get_bounding_box_abs_coordinates(
        self, bounding_box: BoundingBox, image: MatLike
    ) -> tuple[int, int, int, int]:
        image_height, image_width = image.shape[0:2]
        x1 = int(round(bounding_box["x1"] * image_width))
        y1 = int(round(bounding_box["y1"] * image_height))
        x2 = int(round(bounding_box["x2"] * image_width))
        y2 = int(round(bounding_box["y2"] * image_height))
        return (x1, y1, x2, y2)

    def extract_to_str(
        self,
        results: list[Any] | list[dict[str, Any]] | list[str] | list[list[Any]],
    ) -> str:
        text = ""
        for result in results:
            if isinstance(result, str):
                text = text + result + " "
        text = text.strip().lower()
        return text
