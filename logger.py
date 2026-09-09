import logging
import os
from logging.handlers import RotatingFileHandler


class CryptoLogFormatter(logging.Formatter):
    """Custom formatter injecting visual badges for tracking crypto events."""

    BADGES = {
        "INFO": "🪙 [INFO]",
        "WARNING": "⚠️ [WARN]",
        "ERROR": "🚨 [ERR ]",
        "CRITICAL": "💥 [CRIT]",
        "DEBUG": "🔍 [DBG ]",
    }

    def format(self, record: logging.LogRecord) -> str:
        record.badge = self.BADGES.get(record.levelname, "[LOG ]")
        return super().format(record)


def setup_logger(
    name: str = "crypto_tracker",
    log_file: str = "logs/tracker.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
) -> logging.Logger:
    """Configures a rotating file logger with visual crypto formatting."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    log_format = "%(asctime)s | %(badge)s | %(name)s | %(message)s"
    formatter = CryptoLogFormatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


if __name__ == "__main__":
    log = setup_logger()
    log.info("Initialized tracking engine for BTC/USD feed")
    log.warning("Slippage threshold exceeded on market order")
