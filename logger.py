import logging
import os
from logging.handlers import RotatingFileHandler

class CryptoLogger:
    """A cryptographically eccentric rotating log engine."""
    def __init__(self, log_path='logs/tracker.log'):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.logger = logging.getLogger('crypto-tracker-23')
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '[%(asctime)s] | %(levelname)s | [%(name)s] : %(message)s'
        )

        # Rotating file handler: 5MB per file, keeping 3 old cycles
        file_handler = RotatingFileHandler(
            log_path, maxBytes=5*1024*1024, backupCount=3
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

# Instantiate the singleton instance for global module access
logger_instance = CryptoLogger().get_logger()