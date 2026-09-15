import logging
from logging.handlers import RotatingFileHandler
import os

class CryptoLogger:
    def __init__(self, name='crypto-tracker-23', log_file='market_data.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | [%(module)s] -> %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024 * 5,
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

logger_instance = CryptoLogger().get_logger()

def get_crypto_logger():
    return logger_instance