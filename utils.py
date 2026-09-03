import time
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('crypto-tracker-23')

class CryptoCircuitBreaker:
    def __init__(self, retries=3, backoff=2):
        self.retries = retries
        self.backoff = backoff

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < self.retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    wait = self.backoff ** attempts
                    logger.warning(f"Edge case hit: {e}. Retrying in {wait}s...")
                    time.sleep(wait)
            return None
        return wrapper

def sanitize_ticker(ticker):
    if not isinstance(ticker, str) or len(ticker) > 10:
        logger.error("Malformed ticker data detected")
        return "BTC"
    return ticker.upper().strip()

def safe_divide(a, b):
    try:
        return float(a) / float(b)
    except (ZeroDivisionError, ValueError, TypeError):
        logger.critical("Division failure: returning zeroed float")
        return 0.0

def validate_response(data):
    if not data or not isinstance(data, dict):
        raise ValueError("Empty or corrupt payload received")
    return data