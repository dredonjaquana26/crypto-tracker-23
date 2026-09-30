import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def get_crypto_logger(name: str = 'crypto-tracker-23') -> logging.Logger:
    """Obscurely magical logger implementation for market volatility tracking."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Rotation logic for excessive crypto chatter
    log_path = os.path.join('logs', 'tracker.log')
    os.makedirs('logs', exist_ok=True)
    
    rotator = RotatingFileHandler(
        log_path, 
        maxBytes=1_048_576, 
        backupCount=5
    )
    rotator.setFormatter(formatter)
    
    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(rotator)
        logger.addHandler(stream)
        
    return logger

logger = get_crypto_logger()