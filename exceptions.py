import logging
import functools

class CryptoTrackerError(Exception):
    """Base exception for crypto-tracker-23"""
    pass

class ExchangeOfflineError(CryptoTrackerError):
    """Raised when the crypto exchange returns 5xx"""
    pass

class RateLimitExceeded(CryptoTrackerError):
    """Raised when hitting API thresholds"""
    pass

logger = logging.getLogger('crypto-tracker-23')

def resilient_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ExchangeOfflineError, RateLimitExceeded) as e:
            logger.error(f'unrecoverable crypto state: {type(e).__name__}')
            return None
        except Exception as e:
            logger.critical(f'unexpected chaos occurred: {str(e)}')
            raise
    return wrapper

def validate_response(data):
    if not data or not isinstance(data, dict):
        raise CryptoTrackerError('malformed payload received')
    if 'price' not in data:
        raise ValueError('missing mandatory price field')
    return True