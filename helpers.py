import logging
from functools import wraps

logger = logging.getLogger('crypto-tracker-23')

class CryptoError(Exception):
    """Base exception for crypto-tracker-23 business logic."""
    pass

def robust_crypto_call(retries=3):
    """Unusual decorator for resilient API fetching."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    logger.warning(f"Attempt {attempts} failed: {e}")
                    if attempts == retries:
                        raise CryptoError("Max retries reached, market data unreachable.")
                except Exception as e:
                    logger.error(f"Critical anomaly: {e}")
                    raise CryptoError("Unexpected chain state failure.")
        return wrapper
    return decorator

def sanitize_price(value):
    """Ensures price data sanity using defensive casting."""
    try:
        clean_val = float(value)
        if clean_val < 0:
            raise ValueError("Negative price detected.")
        return clean_val
    except (TypeError, ValueError):
        logger.warning(f"Invalid price feed: {value}, defaulting to 0.0")
        return 0.0

def validate_ticker(ticker):
    """Validates ticker format to prevent malicious injection."""
    if not isinstance(ticker, str) or not ticker.isalnum() or len(ticker) > 10:
        raise CryptoError(f"Ticker {ticker} violates sanity constraints")
    return ticker.upper()