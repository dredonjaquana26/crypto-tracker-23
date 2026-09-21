import logging
import os
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        record.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record.crypto_icon = '₿' if record.levelno == logging.INFO else '⚠'
        return f"[{record.timestamp}] {record.crypto_icon} {record.levelname}: {record.getMessage()}"

def get_crypto_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(CryptoFormatter())
        logger.addHandler(handler)
        logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
    return logger

log = get_crypto_logger('crypto-tracker-23')

def track_event(message: str, payload: dict = None):
    formatted_data = " | ".join([f"{k}={v}" for k, v in (payload or {}).items()])
    log.info(f"{message} -> {formatted_data}")

def alert_volatile(price_change: float):
    if abs(price_change) > 5.0:
        log.warning(f"High volatility detected: {price_change}%")