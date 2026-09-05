import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto-tracker-23', log_file='tracker.log'):
    # ensure logs folder exists
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    path = os.path.join(log_dir, log_file)
    
    # custom formatter for crypto-specific context
    formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # rotation setup: 5mb per file, max 3 backups
    handler = RotatingFileHandler(
        path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # check handlers to prevent double-logging during module reloads
    if not logger.handlers:
        logger.addHandler(handler)
        # stream for local console monitoring
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

logger = get_crypto_logger()