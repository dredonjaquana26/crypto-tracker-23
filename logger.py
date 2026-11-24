import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name: str = "crypto-tracker-23") -> logging.Logger:
    """
    A logger factory that rotates files like a blockchain cycle.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # Rotating file handler: 1MB per file, 5 backup generations
        handler = RotatingFileHandler(
            os.path.join(log_dir, "crypto.log"),
            maxBytes=1_048_576,
            backupCount=5,
            encoding="utf-8"
        )
        
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add console output for local debugging
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger