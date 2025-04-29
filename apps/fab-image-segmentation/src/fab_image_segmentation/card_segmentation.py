import logging
import os

import cv2
from pythonjsonlogger.json import JsonFormatter

from fab_image_segmentation.card_config import (
    CardConfig,
    CardRegionConfig,
    fab_card_config,
)

logger = logging.getLogger(__name__)


def run():
    log_level = os.environ["LOG_LEVEL"]
    src_dir = os.environ["SRC_DIR"]
    target_dir = os.environ["TARGET_DIR"]

    init_logging(log_level)
    segment_cards(src_dir, target_dir)


def init_logging(log_level: str):
    handler = logging.StreamHandler()
    formatter = JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"levelname": "level", "asctime": "timestamp"},
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level.upper())


def segment_cards(src_dir: str, target_dir: str):
    file_paths = get_file_paths(src_dir)
    for file_path in file_paths:
        logger.info("segmenting card", extra={"file_path": file_path})
        segment_card(fab_card_config, file_path, target_dir)


def get_file_paths(dir: str) -> list[str]:
    files = os.listdir(dir)
    file_paths = [os.path.join(dir, file) for file in files]
    return file_paths


def segment_card(card_config: CardConfig, src_img: str, target_dir: str):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    os.chdir(target_dir)

    file_name = os.path.basename(src_img)
    file_base_name = file_name.split(".")[0]
    file_extension = file_name.split(".")[1]
    image = cv2.imread(src_img)
    # image_height, image_width = image.shape[0:2]
    for region_config in card_config["regions"]:
        (x1, y1, x2, y2) = get_bounding_box_abs_positions(region_config, image)
        image_segment = image[y1:y2, x1:x2]
        segment_height, segment_width = image_segment.shape[0:2]
        # target_filename = f"{file_base_name}__{region_config['name']}__w{segment_width}__h{segment_height}.{file_extension}"
        target_filename = f"{file_base_name}__{region_config['name']}.{file_extension}"
        target_img_path = os.path.join(target_dir, target_filename)
        if os.path.exists(target_img_path):
            logger.info(
                "image already exits, skipping",
                extra={"target_filename": target_filename},
            )
            continue
        gray = cv2.cvtColor(image_segment, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        # target_img_path = os.path.join(target_dir, output_filename)
        # print(target_img_path)
        logger.info("saving image", extra={"target_filename": target_filename})
        cv2.imwrite(target_filename, enhanced)


def get_bounding_box_abs_positions(
    region_config: CardRegionConfig, image: cv2.typing.MatLike
) -> tuple[int, int, int, int]:
    image_height, image_width = image.shape[0:2]
    x1 = int(round(region_config["bounding_box"]["x1"] * image_width))
    y1 = int(round(region_config["bounding_box"]["y1"] * image_height))
    x2 = int(round(region_config["bounding_box"]["x2"] * image_width))
    y2 = int(round(region_config["bounding_box"]["y2"] * image_height))
    return (x1, y1, x2, y2)
