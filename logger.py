import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

class CryptoLogger:
    def __init__(self, name='crypto-tracker-23', log_file='tracker.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        Path('logs').mkdir(exist_ok=True)
        path = Path('logs') / log_file
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s'
        )

        file_handler = RotatingFileHandler(
            path, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

def setup_crypto_logger():
    return CryptoLogger().get_logger()

logger = setup_crypto_logger()