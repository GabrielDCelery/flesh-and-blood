import os
import zipfile
from urllib.request import urlretrieve

from common import TextExtractorJSONLogger, TextExtractsSQLiteStorage


def main():
    log_level = os.environ["LOG_LEVEL"]
    models_dir = os.environ["MODELS_DIR"]
    model_name = os.environ["MODEL_NAME"]
    language_model_url = os.environ["LANGUAGE_MODEL_URL"]
    text_detection_model_url = os.environ["TEXT_DETECTION_MODEL_URL"]
    db_path = os.environ["DB_PATH"]

    storage = TextExtractsSQLiteStorage(db_path)
    logger = TextExtractorJSONLogger(log_level)

    logger.get().info(f"create text extractor database", extra={"db_path": db_path})

    storage.create_db()

    target_dir_path = os.path.join(models_dir, model_name)

    os.makedirs(target_dir_path, exist_ok=True)

    language_model_file_name = language_model_url.split("/")[-1]

    logger.get().info(
        f"retrieving lanugage model",
        extra={"language_model_url": language_model_url},
    )

    urlretrieve(language_model_url, language_model_file_name)

    text_detection_model_file_name = text_detection_model_url.split("/")[-1]

    logger.get().info(
        f"retrieving text detection model",
        extra={"text_detection_model_url": text_detection_model_url},
    )

    urlretrieve(text_detection_model_url, text_detection_model_file_name)

    with zipfile.ZipFile(language_model_file_name, "r") as zip_ref:
        logger.get().info(
            f"extract lanugage model",
            extra={
                "target_dir_path": target_dir_path,
                "language_model_file_name": language_model_file_name,
            },
        )
        zip_ref.extractall(target_dir_path)

    with zipfile.ZipFile(text_detection_model_file_name, "r") as zip_ref:
        logger.get().info(
            f"extract lanugage model",
            extra={
                "target_dir_path": target_dir_path,
                "text_detection_model_file_name": text_detection_model_file_name,
            },
        )
        zip_ref.extractall(target_dir_path)


if __name__ == "__main__":
    main()
