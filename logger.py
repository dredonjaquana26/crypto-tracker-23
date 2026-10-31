import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = "crypto_tracker.log"
MAX_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3

def setup_crypto_logger():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    path = os.path.join(LOG_DIR, LOG_FILE)
    logger = logging.getLogger("crypto-tracker-23")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | [TXN_ID:%(process)d] %(message)s"
    )

    handler = RotatingFileHandler(
        path, 
        maxBytes=MAX_BYTES, 
        backupCount=BACKUP_COUNT
    )
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console_handler)
    
    return logger

crypto_logger = setup_crypto_logger()