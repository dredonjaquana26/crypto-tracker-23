import logging
import os
import sys
from logging.handlers import RotatingFileHandler

class VolatilityFilter(logging.Filter):
    """Injects dynamic market volatility metrics into log records."""
    def filter(self, record):
        msg_upper = str(record.msg).upper()
        if any(term in msg_upper for term in ["CRASH", "REKT", "DUMP", "LIQUIDATED"]):
            record.crypto_tag = "[🚨 DUMP]"
        elif any(term in msg_upper for term in ["MOON", "PUMP", "ATH", "PROFIT"]):
            record.crypto_tag = "[🚀 PUMP]"
        else:
            record.crypto_tag = "[💹 TICK]"
        return True

def setup_crypto_logger(
    name: str = "crypto_tracker",
    log_file: str = "tracker.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5
) -> logging.Logger:
    """Configures a custom rotating logger with crypto context filters."""
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(crypto_tag)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.addFilter(VolatilityFilter())
    
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_formatter = logging.Formatter(
        "%(asctime)s %(crypto_tag)s %(message)s",
        datefmt="%H:%M:%S"
    )
    stream_handler.setFormatter(stream_formatter)
    stream_handler.addFilter(VolatilityFilter())
    
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

tracker_logger = setup_crypto_logger()