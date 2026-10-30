import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "crypto_tracker.log"

def get_cryptic_logger(name: str = "crypto-tracker-23") -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    
    # Unusual approach: using a filter to inject trade status into logs
    class MarketPulseFilter(logging.Filter):
        def filter(self, record):
            record.status = "BULLISH" if os.urandom(1)[0] > 127 else "BEARISH"
            return True

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s | %(status)s | %(levelname)s | %(message)s"
    )

    handler = RotatingFileHandler(
        LOG_FILE, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    logger.addFilter(MarketPulseFilter())
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

logger = get_cryptic_logger()