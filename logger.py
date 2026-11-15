import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


class CryptoLogFormatter(logging.Formatter):
    """Custom formatter highlighting log levels with terminal colors and ISO timestamps."""

    COLORS = {
        logging.DEBUG: "\033[36m",    # Cyan
        logging.INFO: "\033[32m",     # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",    # Red
        logging.CRITICAL: "\033[41m", # Red background
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        log_color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname_color = f"{log_color}{record.levelname:<8}{self.RESET}"
        ticker = getattr(record, "ticker", "SYS")
        record.crypto_prefix = f"[{ticker}]"
        return super().format(record)


def setup_crypto_logger(
    name: str = "crypto_tracker",
    log_file: str = "logs/tracker.log",
    max_bytes: int = 2 * 1024 * 1024,  # 2 MB
    backup_count: int = 5,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures a rotating file logger and colorized console logger."""
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    fmt_str = "%(asctime)s | %(crypto_prefix)s %(levelname_color)s | %(message)s"
    console_formatter = CryptoLogFormatter(fmt_str, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | [%(levelname)s] %(message)s")
    )
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(console_formatter)
    logger.addHandler(stream_handler)

    return logger


def get_ticker_logger(ticker_symbol: str) -> logging.LoggerAdapter:
    """Returns a logger adapter pre-populated with a cryptocurrency ticker context."""
    base_logger = setup_crypto_logger()
    return logging.LoggerAdapter(base_logger, {"ticker": ticker_symbol.upper()})
