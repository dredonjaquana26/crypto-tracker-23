import os
import logging
from logging.handlers import RotatingFileHandler

class CryptoSentimentFormatter(logging.Formatter):
    """Custom formatter highlighting market sentiment from logs."""
    def format(self, record):
        original_msg = record.msg
        if isinstance(record.msg, str):
            msg_lower = record.msg.lower()
            if "pump" in msg_lower or "high" in msg_lower or "bull" in msg_lower:
                record.msg = f"📈 {original_msg} [BULLISH]"
            elif "dump" in msg_lower or "low" in msg_lower or "bear" in msg_lower:
                record.msg = f"📉 {original_msg} [BEARISH]"
            elif record.levelno >= logging.WARNING:
                record.msg = f"🚨 {original_msg}"
            else:
                record.msg = f"⚡ {original_msg}"
        formatted = super().format(record)
        record.msg = original_msg
        return formatted

def setup_crypto_logger(
    name: str = "crypto_tracker",
    log_file: str = "crypto_tracker.log",
    max_bytes: int = 5242880,
    backup_count: int = 3
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.hasHandlers():
        logger.handlers.clear()
    console_handler = logging.StreamHandler()
    console_formatter = CryptoSentimentFormatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_formatter = CryptoSentimentFormatter(
        fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger