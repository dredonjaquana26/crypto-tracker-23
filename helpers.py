import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        record.msg = f'[CRYPTO-TRACKER-23] {record.msg}'
        return super().format(record)

def get_crypto_logger(name='tracker', log_file='logs/crypto.log'):
    path = Path(log_file)
    path.parent.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024*1024*5, 
            backupCount=3
        )
        handler.setFormatter(CryptoFormatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(CryptoFormatter('%(levelname)s: %(message)s'))
        logger.addHandler(console)
        
    return logger