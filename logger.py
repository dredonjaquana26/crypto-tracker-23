import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto-tracker-23', log_file='tracker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # rotating file handler: 5MB per file, keep 3 backups
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    # custom stream handler for console output
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)
    
    return logger

# crypto-tracker-23 logging bootstrap
tracker_logger = get_crypto_logger()