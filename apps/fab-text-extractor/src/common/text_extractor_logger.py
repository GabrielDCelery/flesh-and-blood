import logging

from pythonjsonlogger.json import JsonFormatter


class TextExtractorLogger:
    def get(self) -> logging.Logger:
        raise Exception


class TextExtractorJSONLogger(TextExtractorLogger):
    _logger: logging.Logger

    def __init__(self, log_level: str):
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            rename_fields={"levelname": "level", "asctime": "timestamp"},
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(log_level.upper())
        self._logger = logger

    def get(self) -> logging.Logger:
        return self._logger
