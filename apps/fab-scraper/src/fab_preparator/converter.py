import os

from PIL import Image

from fab_preparator.logs import get_logger

VALID_EXTENSIONS = {"jpg", "jpeg", "bmp", "gif", "tiff", "webp"}


def convert_images_to_png(src_dir: str, target_dir: str) -> None:
    logger = get_logger()
    os.makedirs(target_dir, exist_ok=True)
    abs_img_paths = get_valid_image_full_paths(src_dir)
    for abs_img_path in abs_img_paths:
        file_name = os.path.basename(abs_img_path)
        file_base = file_name.split(".")[0]
        new_file_name = f"{file_base}.png"
        target_path = os.path.join(target_dir, new_file_name)
        try:
            with Image.open(abs_img_path) as img:
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                img.save(target_path, "PNG")
                logger.info(
                    f"prepared and saved image", extra={"target_path": target_path}
                )
        except Exception as e:
            logger.error(
                f"failed processing image: {str(e)}",
                extra={"abs_img_path": abs_img_path},
                exc_info=True,
            )


def get_valid_image_full_paths(src_dir: str) -> list[str]:
    abs_img_paths: list[str] = []
    for dirpath, _, file_names in os.walk(src_dir):
        for file_name in file_names:
            file_ext = file_name.split(".")[-1].lower()
            if file_ext not in VALID_EXTENSIONS:
                continue
            full_path = os.path.join(dirpath, file_name)
            abs_img_paths.append(full_path)
    return abs_img_paths
