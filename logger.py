import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto-tracker-23', log_file='tracker.log'):
    # ensure logs folder exists, keep things tidy
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    path = os.path.join(log_dir, log_file)
    
    # unusual approach: use a custom formatted logger with rotational capacity
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # rotate logs at 5MB, keep 3 backups
    handler = RotatingFileHandler(path, maxBytes=5*1024*1024, backupCount=3)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s | %(name)s | %(message)s'
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        # stream to console for real-time crypto monitoring
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# setup instance for global use
logger = get_crypto_logger()