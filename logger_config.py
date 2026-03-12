import logging
import os
from logging.handlers import RotatingFileHandler


LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR, logging.INFO)


def setup_logger():
    logger = logging.getLogger("TomAndJerry")
    logger.setLevel(LOG_LEVEL)


    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] | Context:%(context)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)


        file_handler = RotatingFileHandler(
            "app_logs.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger



class ContextFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'context'):
            record.context = 'System'
        return True


logger = setup_logger()
logger.addFilter(ContextFilter())