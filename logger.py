import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def get_crypto_logger(name='crypto-tracker-23', log_file='market_data.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] >> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # rotating handler: max 5mb per file, keep 3 backups
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)

    return logger

# global tracker logger instance
crypto_logger = get_crypto_logger()