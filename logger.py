import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE = Path('logs/crypto_tracker.log')

class CryptoFormatter(logging.Formatter):
    COLORS = {'DEBUG': '₿', 'INFO': '🚀', 'WARNING': '⚠️', 'ERROR': '🔥', 'CRITICAL': '💀'}
    
    def format(self, record):
        record.emoji = self.COLORS.get(record.levelname, '📈')
        return super().format(record)

def setup_logger(name: str = 'crypto-tracker-23') -> logging.Logger:
    LOG_FILE.parent.mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    handler = RotatingFileHandler(
        LOG_FILE, 
        maxBytes=1024*1024*5, 
        backupCount=3
    )
    
    formatter = CryptoFormatter('%(asctime)s - %(emoji)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger