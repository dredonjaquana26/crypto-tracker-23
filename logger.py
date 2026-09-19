import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class CryptoLogger:
    def __init__(self, name: str = 'crypto-tracker-23', path: str = 'logs/tracker.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        handler = RotatingFileHandler(
            path, 
            maxBytes=1024 * 1024 * 5,
            backupCount=3
        )
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | [%(name)s] -> %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self) -> logging.Logger:
        return self.logger

def setup_global_logger():
    return CryptoLogger().get_logger()