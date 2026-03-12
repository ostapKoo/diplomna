import logging
import os
from logging.handlers import RotatingFileHandler
from contextvars import ContextVar

# sentry
try:
    import sentry_sdk
    from sentry_sdk.integrations.logging import LoggingIntegration


    SENTRY_DSN = os.getenv("SENTRY_DSN",
                           "https://2bd4ee5282e962214c6063842c12aee8@o4511031676108800.ingest.de.sentry.io/4511031683645520")

    if SENTRY_DSN:
        sentry_logging = LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR
        )
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[sentry_logging],
            traces_sample_rate=1.0
        )
        print("✅ Sentry успішно ініціалізовано!")
except ImportError:
    print("⚠️ Бібліотеку sentry-sdk не встановлено. Логи будуть лише локальними.")


trace_id_var = ContextVar("trace_id", default="SYSTEM")


LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR, logging.INFO)


def setup_logger():
    logger = logging.getLogger("TomAndJerry")
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | TraceID: %(trace_id)s | [%(filename)s:%(lineno)d] | Context:%(context)s | %(message)s',
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


class AdvancedContextFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_var.get()
        if not hasattr(record, 'context'):
            record.context = 'System'
        return True


logger = setup_logger()
logger.addFilter(AdvancedContextFilter())