import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto-tracker-23'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | [BLOCKCHAIN] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    log_path = os.path.join(os.getcwd(), 'logs', 'tracker.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Unusual approach: size-based rotation with max 5 backup files
    file_handler = RotatingFileHandler(
        log_path, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Instantiate for global use across crypto-tracker-23
logger = get_crypto_logger()