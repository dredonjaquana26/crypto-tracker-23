import time
import functools
import random
import logging

logger = logging.getLogger('crypto-tracker-23')

def exponential_backoff(max_attempts=3, base_delay=1.0, jitter=True):
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
                        logger.error(f'failed after {attempts} attempts: {e}')
                        raise
                    
                    delay = base_delay * (2 ** (attempts - 1))
                    if jitter:
                        delay += random.uniform(0, 0.5 * delay)
                    
                    logger.warning(f'retry {attempts}/{max_attempts} in {delay:.2f}s...')
                    time.sleep(delay)
        return wrapper
    return decorator

def fetch_with_retry(func):
    return exponential_backoff(max_attempts=5, base_delay=0.5)(func)