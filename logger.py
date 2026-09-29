import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str = 'crypto-tracker-23') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_path = os.path.join(log_dir, f'{name}.log')
        handler = RotatingFileHandler(
            file_path, 
            maxBytes=5*1024*1024, 
            backupCount=3,
            encoding='utf-8'
        )
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

logger = get_crypto_logger()