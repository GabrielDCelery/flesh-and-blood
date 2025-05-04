import glob
import json
import os

from common import TextExtractsSQLiteStorage
from common.text_extractor_logger import TextExtractorJSONLogger
from fab_extract.card_classifier import CardClassifier


def main():
    log_level = os.environ["LOG_LEVEL"]
    img_src_dir = os.environ["IMG_SRC_DIR"]
    models_dir = os.environ["MODELS_DIR"]
    db_path = os.environ["DB_PATH"]

    store = TextExtractsSQLiteStorage(db_path)
    logger = TextExtractorJSONLogger(log_level)
    extractor = CardClassifier(models_dir, store, logger)

    src_images = glob.glob(os.path.join(img_src_dir, "*.png"))

    for src_img in src_images:
        extractor.extract_details(src_img)
    store.close()


if __name__ == "__main__":
    main()
