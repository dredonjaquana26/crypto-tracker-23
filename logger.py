import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class CryptoLogger:
    """Custom logger for crypto-tracker-23 using rotational mechanics."""
    def __init__(self, name="crypto_tracker", log_dir="logs"):
        self.name = name
        self.log_dir = log_dir
        self._ensure_dir()
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self._configure_handler()

    def _ensure_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _configure_handler(self):
        log_file = os.path.join(self.log_dir, f"{self.name}.log")
        handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | [%(name)s] >> %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

def setup_crypto_logger():
    return CryptoLogger().get_logger()

logger = setup_crypto_logger()