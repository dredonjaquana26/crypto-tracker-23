import logging
from logging.handlers import RotatingFileHandler
import sys
import os

class CryptoLogger:
    def __init__(self, name='crypto-tracker-23', log_file='tracker.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] -> %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console stream handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Rotating file handler (5MB per file, keep 3 backups)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5*1024*1024, backupCount=3
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

# Singleton instance for quick access
logger_instance = CryptoLogger().get_logger()

def get_crypto_logger():
    return logger_instance