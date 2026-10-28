import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE = Path('logs/crypto_tracker.log')
LOG_FILE.parent.mkdir(exist_ok=True)

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        record.msg = f'🚀 [CRYPTO-TRACKER] {record.msg}'
        return super().format(record)

def setup_logger(name: str = 'crypto_logger') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        handler = RotatingFileHandler(
            LOG_FILE, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        
        formatter = CryptoFormatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()