import glob
import json
import os

from common import TextExtractsSQLiteStorage
from fab_extract.card_classifier import CardClassifier
from fab_extract.logs import get_logger, init_logger


def main():
    log_level = os.environ["LOG_LEVEL"]
    img_src_dir = os.environ["IMG_SRC_DIR"]
    models_dir = os.environ["MODELS_DIR"]
    db_path = os.environ["DB_PATH"]
    init_logger(log_level)
    logger = get_logger()
    src_images = glob.glob(os.path.join(img_src_dir, "*.png"))
    store = TextExtractsSQLiteStorage(db_path)
    extractor = CardClassifier(models_dir, store)
    for src_img in src_images:
        # file_name = os.path.basename(src_img)
        card_info = extractor.extract_details(src_img)
        logger.info(
            f"finished extracting data from image",
            extra={"src_img": src_img, "data": json.dumps(card_info)},
        )


if __name__ == "__main__":
    main()
