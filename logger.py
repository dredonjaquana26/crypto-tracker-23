import logging
import os
import sys
from logging.handlers import RotatingFileHandler


class CryptoLogFormatter(logging.Formatter):
    """Custom log formatter injecting market status badges."""

    LEVEL_ICONS = {
        logging.DEBUG: "🔍 [TRACE]",
        logging.INFO: "⚡ [TICK]",
        logging.WARNING: "⚠️ [VOLATILE]",
        logging.ERROR: "💥 [LIQUIDATED]",
        logging.CRITICAL: "🚨 [RUGPULL]",
    }

    def format(self, record: logging.LogRecord) -> str:
        icon = self.LEVEL_ICONS.get(record.levelno, "🟢")
        record.crypto_prefix = f"{icon} [{record.name}]"
        return super().format(record)


def setup_crypto_logger(
    name: str = "crypto_tracker",
    log_file: str = "logs/crypto_feed.log",
    max_bytes: int = 512 * 1024,
    backup_count: int = 5,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures a self-rotating log stream for real-time crypto telemetry."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        return logger

    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    formatter = CryptoLogFormatter(
        fmt="%(asctime)s | %(crypto_prefix)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


main_logger = setup_crypto_logger()
