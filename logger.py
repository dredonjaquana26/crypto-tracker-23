import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        record.msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🪙 {record.msg}"
        return super().format(record)

def setup_crypto_logger(name='crypto-tracker-23', log_file='market_data.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        
        formatter = CryptoFormatter('%(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

logger = setup_crypto_logger()