import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

class CryptoLogger:
    """Custom logger for crypto-tracker-23 with file rotation."""
    def __init__(self, name: str = 'crypto_tracker'):
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / f'{name}.log'
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Rotate at 5MB, keep 3 historical backups
        handler = RotatingFileHandler(
            self.log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.addHandler(console)

    def get_logger(self) -> logging.Logger:
        return self.logger

def setup_global_logger():
    return CryptoLogger().get_logger()