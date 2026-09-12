import logging
from logging.handlers import RotatingFileHandler
import os

def setup_crypto_logger(name="crypto_tracker", log_file="crypto.log", max_bytes=1048576, backup_count=5):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger

    os.makedirs("logs", exist_ok=True)
    file_path = os.path.join("logs", log_file)

    class CryptoFormatter(logging.Formatter):
        def format(self, record):
            symbol = "🚀" if record.levelno == logging.INFO else "⚠️" if record.levelno == logging.WARNING else "💥"
            record.msg = f"[{symbol}] {record.msg}"
            return super().format(record)

    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    formatter = CryptoFormatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler(file_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-safe")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
