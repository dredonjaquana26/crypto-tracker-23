import logging
from logging.handlers import RotatingFileHandler
import os

class CryptoLogger:
    def __init__(self, name='crypto_tracker_23', log_file='market_data.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Custom formatter to track market noise vs signal
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | [CHAIN_ID] | %(message)s')
        
        # 5MB log limit per file, keep 3 backups
        handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Also output to stdout for real-time monitoring
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

# Instantiate for global access in the crypto ecosystem
logger = CryptoLogger().get_logger()