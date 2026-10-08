import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name='crypto-tracker-23', log_file='tracker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [TXN] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Custom rotation logic: 5MB files, keeps 3 backups
        rotator = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        rotator.setFormatter(formatter)
        logger.addHandler(rotator)
        
        # Add a console stream for real-time volatility tracking
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        logger.addHandler(stream)
        
    return logger

# Instantiate for global use
logger = get_crypto_logger()