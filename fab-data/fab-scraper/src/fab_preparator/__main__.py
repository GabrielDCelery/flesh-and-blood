import os

from fab_preparator.converter import convert_images_to_png
from fab_preparator.logs import init_logging


def run() -> None:
    log_level = os.environ["LOG_LEVEL"]
    src_dir = os.environ["SRC_DIR"]
    target_dir = os.environ["TARGET_DIR"]
    init_logging(log_level)
    convert_images_to_png(src_dir, target_dir)
    pass


if __name__ == "__main__":
    run()
