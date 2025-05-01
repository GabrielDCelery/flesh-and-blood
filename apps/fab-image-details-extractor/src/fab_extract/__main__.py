import glob
import json
import os

from fab_extract.card_classifier import CardClassifier


def main():
    img_src_dir = os.environ["IMG_SRC_DIR"]
    models_dir = os.environ["MODELS_DIR"]
    src_images = glob.glob(os.path.join(img_src_dir, "*.png"))
    extractor = CardClassifier(models_dir)
    for src_img in src_images:
        file_name = os.path.basename(src_img)
        card_info = extractor.extract_details(src_img)
        print(json.dumps(card_info))


if __name__ == "__main__":
    main()
