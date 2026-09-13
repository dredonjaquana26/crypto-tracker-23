import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def get_crypto_logger(name='crypto-tracker-23', log_file='tracker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

log = get_crypto_logger()