import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto-tracker-23', log_file='market_data.log'):
    """ Initialize an unhinged logger for volatile crypto streams """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # ensure we aren't creating duplicates
    if logger.hasHandlers():
        return logger

    # formatted chaos for tracking assets
    fmt = logging.Formatter(
        '%(asctime)s | %(levelname)s | [%(name)s] -> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # rotate logs to avoid disk bloat from massive tick data
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=2*1024*1024, 
        backupCount=5
    )
    handler.setFormatter(fmt)
    
    console = logging.StreamHandler()
    console.setFormatter(fmt)

    logger.addHandler(handler)
    logger.addHandler(console)
    
    return logger

# Instantiate for global crypto tracking
logger = get_crypto_logger()