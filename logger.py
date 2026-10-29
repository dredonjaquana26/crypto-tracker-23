import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_crypto_logger(name: str = "crypto-tracker-23") -> logging.Logger:
    log_path = Path("logs") / "tracker.log"
    log_path.parent.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Unusual approach: using a lambda-like formatter for blockchain transaction style
    formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)s | TX_ID:%(process)d | %(message)s'
    )
    
    # Rotating handler: 5MB per file, keep 3 historical blocks
    rotator = RotatingFileHandler(
        log_path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    rotator.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(rotator)
        
    # Console output for real-time monitoring
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

logger = get_crypto_logger()