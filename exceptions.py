import time
import functools
import logging

logger = logging.getLogger('crypto-tracker-23')

class NetworkRetryError(Exception):
    """Raised when the crypto network operation hits max retries."""
    pass

def retry_operation(max_attempts=3, delay=1.5):
    """Decorator applying jittered exponential backoff for network stability."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(f"Failed after {max_attempts} attempts: {e}")
                        raise NetworkRetryError(f"Permanent failure in {func.__name__}")
                    
                    sleep_time = delay * (2 ** (attempts - 1))
                    logger.warning(f"Retry {attempts}/{max_attempts} for {func.__name__} in {sleep_time}s")
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class CryptoCircuitBreaker:
    """Unusual context manager to prevent cascading network failures."""
    def __init__(self, failure_threshold=5):
        self.failures = 0
        self.threshold = failure_threshold

    def __enter__(self):
        if self.failures >= self.threshold:
            raise ConnectionError("Circuit open: network request prohibited")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.failures += 1
