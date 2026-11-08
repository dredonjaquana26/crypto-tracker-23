import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        record.crypto_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return super().format(record)

def setup_logger(name='crypto-tracker-23', log_dir='logs'):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    path = os.path.join(log_dir, f'{name}.log')
    handler = RotatingFileHandler(
        path, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )

    formatter = CryptoFormatter(
        '[%(crypto_stamp)s] [%(levelname)s] [%(name)s]: %(message)s'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger

log = setup_logger()