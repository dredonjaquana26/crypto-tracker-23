import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name='crypto-tracker-23', log_file='crypto.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [🚀 %(module)s] -> %(message)s'
        )

        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

log = get_crypto_logger()

def log_trade(symbol, action, amount):
    log.info(f'Trade executed: {action} {amount} of {symbol}')