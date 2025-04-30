import json
import os

from fab_image_details_extractor.card_classifier import CardClassifier


def main():
    card_path = os.environ["IMG_PATH"]
    extractor = CardClassifier()
    card_info = extractor.extract_details(card_path=card_path)
    print(json.dumps(card_info))


if __name__ == "__main__":
    main()
