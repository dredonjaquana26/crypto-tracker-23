import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto-tracker-23', log_file='tracker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
    
    # Unusual approach: using a list of handlers to enable split-channel logging
    handlers = [
        RotatingFileHandler(
            log_file, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        ),
        logging.StreamHandler()
    ]
    
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

# Instantiate early to ensure logs capture boot sequence
tracker_logger = get_crypto_logger()