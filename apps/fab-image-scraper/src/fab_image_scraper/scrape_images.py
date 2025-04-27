import asyncio
import logging
import os
import random

import aiohttp
import requests
from aiohttp.client import ClientSession
from bs4 import BeautifulSoup, Tag

from fab_image_scraper import logging_config

logger = logging.getLogger(__name__)


class ImageDownloadError(Exception):
    pass


class InvalidImageURLError(Exception):
    pass


def main():
    # Your main application logic here
    url = os.environ["PAGE_URL"]
    download_dir = os.environ["DOWNLOAD_DIR"]
    log_level = os.environ["LOG_LEVEL"]
    concurrency = int(os.environ["DOWNLOAD_CONCURRENCY"])

    logging_config.setup_logging(log_level)
    logger.info(
        "Starting the application", extra={"url": url, "download_dir": download_dir}
    )
    image_urls = get_image_urls_from_page(url)
    create_download_dir(download_dir)
    asyncio.run(download_images(image_urls, download_dir, concurrency))
    return


def get_image_urls_from_page(url: str) -> list[str]:
    # Headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        image_urls: list[str] = []

        for img in soup.find_all("img"):
            if not isinstance(img, Tag):
                continue
            src = img.get("src")
            if not isinstance(src, str):
                continue
            image_urls.append(src)

        return image_urls

    except Exception as e:
        print(f"Error fetching page: {str(e)}")
        return []


def create_download_dir(download_dir: str) -> None:
    os.makedirs(download_dir, exist_ok=True)
    return


async def download_images(
    image_urls: list[str], download_dir: str, concurrency: int
) -> None:
    # Create a semaphore that limits concurrent downloads to 1
    semaphore = asyncio.Semaphore(concurrency)

    async def download_with_semaphore(
        session: ClientSession, image_url: str, download_dir: str, concurrency: int
    ) -> None:
        async with semaphore:
            await download_image(session, image_url, download_dir, concurrency)

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(
                download_with_semaphore(session, image_url, download_dir, concurrency)
            )
            for image_url in image_urls
        ]
        await asyncio.gather(*tasks)


async def download_image(
    session: ClientSession, image_url: str, download_dir: str, concurrency: int
) -> None:
    """
    Download a single image from a given URL

    Args:
        session: The aiohttp client session
        image_url: URL of the image we want to download
        download_dir: Directory to save the image to

    Raises:
        ImageDownloadError: If the download fails
        InvalidImageURLError: If the URL is invalid
    """
    file_name = image_url.split("/")[-1]
    try:
        file_path = os.path.join(download_dir, file_name)
        is_file = os.path.isfile(file_path)
        if is_file:
            logger.info(
                f"skipping downloading already existing file",
                extra={"file_name": file_name, "file_path": file_path},
            )
            return
        is_valid_url = image_url.startswith(("http://", "https://"))
        if not is_valid_url:
            raise InvalidImageURLError(f"invalis URL scheme for {image_url}")
        async with session.get(image_url) as response:
            if response.status != 200:
                return
            with open(file_path, "wb") as f:
                f.write(await response.read())
                logger.info(f"saved file", extra={"file_path": file_path})
            await asyncio.sleep(random.uniform(1, concurrency))
    except aiohttp.ClientError as e:
        logger.error(
            f"network error downloading image: {e}",
            extra={"image_url": image_url},
            exc_info=True,
        )
        raise ImageDownloadError(f"failed to download {image_url}") from e
    except OSError as e:
        logger.error(
            f"file system error saving file: {e}",
            extra={"file_name": file_name},
            exc_info=True,
        )
        raise ImageDownloadError(f"failed to save {file_name}") from e


if __name__ == "__main__":
    main()
