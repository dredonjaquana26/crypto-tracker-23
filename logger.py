import logging
from logging.handlers import RotatingFileHandler
import sys

def get_crypto_logger(name='crypto-tracker-23', log_file='tracker.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # The Unusual Twist: Dual-path logging with file rotation and stdout
    fh = RotatingFileHandler(log_file, maxBytes=1048576, backupCount=5)
    fh.setFormatter(formatter)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger

# Instantiate for global access in crypto-tracker-23
log = get_crypto_logger()