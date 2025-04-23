import logging

from pythonjsonlogger.json import JsonFormatter


def setup_logging(log_level: str):
    logger = logging.getLogger()
    logger.setLevel(log_level.upper())
    logHandler = logging.StreamHandler()
    formatter = JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"levelname": "level", "asctime": "timestamp"},
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #     datefmt="%Y-%m-%d %H:%M:%S",
    # )
    return
