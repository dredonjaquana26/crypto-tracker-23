import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {'INFO': '\033[94m', 'ERROR': '\033[91m', 'DEBUG': '\033[92m'}
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, '\033[0m')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f'{color}[{timestamp}] {record.levelname}: {record.getMessage()}\033[0m'

def setup_crypto_logger(name='crypto-tracker-23'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CryptoFormatter())
    
    if not logger.handlers:
        logger.addHandler(console_handler)
    return logger

log = setup_crypto_logger()