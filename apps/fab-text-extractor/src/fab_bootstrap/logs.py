import logging

from pythonjsonlogger.json import JsonFormatter

logger = logging.getLogger(__name__)


def init_logger(log_level: str) -> logging.Logger:
    handler = logging.StreamHandler()
    formatter = JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"levelname": "level", "asctime": "timestamp"},
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level.upper())
    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger(__name__)
