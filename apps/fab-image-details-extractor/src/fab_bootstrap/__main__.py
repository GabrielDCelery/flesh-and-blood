import os
import zipfile
from urllib.request import urlretrieve


def main():
    models_dir = os.environ["MODELS_DIR"]
    language_model_url = os.environ["LANGUAGE_MODEL_URL"]
    text_detection_model_url = os.environ["TEXT_DETECTION_MODEL_URL"]

    target_dir_path = os.path.join(models_dir, "model")

    os.makedirs(target_dir_path, exist_ok=True)

    language_model_file_name = language_model_url.split("/")[-1]

    urlretrieve(language_model_url, language_model_file_name)

    text_detection_model_file_name = text_detection_model_url.split("/")[-1]

    urlretrieve(text_detection_model_url, text_detection_model_file_name)

    with zipfile.ZipFile(language_model_file_name, "r") as zip_ref:
        print(f"ZIP file contents: {zip_ref.namelist()}")

        zip_ref.extractall(target_dir_path)

    with zipfile.ZipFile(text_detection_model_file_name, "r") as zip_ref:
        print(f"ZIP file contents: {zip_ref.namelist()}")

        zip_ref.extractall(target_dir_path)


if __name__ == "__main__":
    main()
