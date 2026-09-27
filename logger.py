import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

def setup_crypto_logger(name: str = 'crypto-tracker-23') -> logging.Logger:
    log_path = Path('logs')
    log_path.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    file_handler = RotatingFileHandler(
        log_path / 'app.log',
        maxBytes=1024 * 1024 * 5,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

logger = setup_crypto_logger()