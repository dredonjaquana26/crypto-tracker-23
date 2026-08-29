import logging
from logging.handlers import RotatingFileHandler
import os

def create_rotating_logger(name="crypto_tracker", log_file="crypto_tracker.log", 
                           max_bytes=5*1024*1024, backup_count=5,
                           level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if logger.handlers:
        logger.handlers.clear()
    
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)
    
    class CryptoContextFilter(logging.Filter):
        def filter(self, record):
            record.crypto_context = "crypto-tracker-23"
            return True
    
    logger.addFilter(CryptoContextFilter())
    
    return logger