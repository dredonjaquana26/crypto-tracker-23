import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def get_crypto_logger(name='crypto-tracker-23', log_file='tracker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # formatter with custom aesthetic
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # stdout for development visibility
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # rotating file handler to prevent disk overflow
    # 5MB per file, keep 3 backups
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    file_path = os.path.join('logs', log_file)
    file_handler = RotatingFileHandler(
        file_path, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # prevent duplicate loggers
    logger.propagate = False
    return logger

# setup instance for global use
logger = get_crypto_logger()