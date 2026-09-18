import time
import functools
import random
import logging

logger = logging.getLogger('crypto-tracker-23')

class NetworkRetry:
    def __init__(self, max_retries=3, base_delay=1.0, backoff=2.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.backoff = backoff

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = self.base_delay
            while retries < self.max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries >= self.max_retries:
                        logger.error(f"Final attempt failed for {func.__name__}: {e}")
                        raise
                    jitter = random.uniform(0, 0.1 * delay)
                    sleep_time = delay + jitter
                    logger.warning(f"Retry {retries}/{self.max_retries} for {func.__name__} after {sleep_time:.2f}s")
                    time.sleep(sleep_time)
                    delay *= self.backoff
        return wrapper

class CryptoNetworkError(Exception):
    """Custom exception for crypto-tracker-23 network anomalies"""
    pass