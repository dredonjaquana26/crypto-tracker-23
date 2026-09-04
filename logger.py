import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto-tracker-23', log_file='crypto.log', max_bytes=1048576, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | [🚀 %(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console output for the terminal enthusiasts
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File rotation for the historical ledger
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Instantiate the global tracker logger
tracker_logger = get_crypto_logger()