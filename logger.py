import logging
import os
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[95m'
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        reset = '\033[0m'
        log_msg = super().format(record)
        return f"{color}[{datetime.now().strftime('%H:%M:%S')}] {record.levelname}: {log_msg}{reset}"

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CryptoFormatter('%(message)s'))
    logger.addHandler(console_handler)

    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    file_handler = logging.FileHandler(f'logs/crypto_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    return logger