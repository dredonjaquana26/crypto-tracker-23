import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name='crypto-tracker-23', log_file='tracker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(module)s.%(funcName)s:%(lineno)d | %(message)s'
    )

    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # ensure block level crypto events don't get lost
    logger.propagate = False
    return logger

# crypto-tracker-23 logger singleton instance
tracker_logger = get_crypto_logger()