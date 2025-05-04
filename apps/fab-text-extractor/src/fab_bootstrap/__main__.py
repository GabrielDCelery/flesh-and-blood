import os
import zipfile
from urllib.request import urlretrieve

from fab_bootstrap.logs import init_logger
from fab_bootstrap.store import create_db


def main():
    log_level = os.environ["LOG_LEVEL"]
    models_dir = os.environ["MODELS_DIR"]
    model_name = os.environ["MODEL_NAME"]
    language_model_url = os.environ["LANGUAGE_MODEL_URL"]
    text_detection_model_url = os.environ["TEXT_DETECTION_MODEL_URL"]
    db_path = os.environ["DB_PATH"]

    logger = init_logger(log_level)

    logger.info(f"create text extractor database", extra={"db_path": db_path})

    create_db(db_path)

    target_dir_path = os.path.join(models_dir, model_name)

    os.makedirs(target_dir_path, exist_ok=True)

    language_model_file_name = language_model_url.split("/")[-1]

    logger.info(
        f"retrieving lanugage model",
        extra={"language_model_url": language_model_url},
    )

    urlretrieve(language_model_url, language_model_file_name)

    text_detection_model_file_name = text_detection_model_url.split("/")[-1]

    logger.info(
        f"retrieving text detection model",
        extra={"text_detection_model_url": text_detection_model_url},
    )

    urlretrieve(text_detection_model_url, text_detection_model_file_name)

    with zipfile.ZipFile(language_model_file_name, "r") as zip_ref:
        logger.info(
            f"extract lanugage model",
            extra={
                "target_dir_path": target_dir_path,
                "language_model_file_name": language_model_file_name,
            },
        )
        zip_ref.extractall(target_dir_path)

    with zipfile.ZipFile(text_detection_model_file_name, "r") as zip_ref:
        logger.info(
            f"extract lanugage model",
            extra={
                "target_dir_path": target_dir_path,
                "text_detection_model_file_name": text_detection_model_file_name,
            },
        )
        zip_ref.extractall(target_dir_path)


if __name__ == "__main__":
    main()
