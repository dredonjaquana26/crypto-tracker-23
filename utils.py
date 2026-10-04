import time
import functools
import random
import logging

logger = logging.getLogger('crypto-tracker-23')

def retry_operation(max_attempts=3, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    jitter = random.uniform(0, 0.5)
                    wait = (backoff ** attempts) + jitter
                    logger.warning(f'attempt {attempts} failed: {e}. retrying in {wait:.2f}s...')
                    if attempts >= max_attempts:
                        logger.error('max retries reached for network operation')
                        raise
                    time.sleep(wait)
        return wrapper
    return decorator

@retry_operation(max_attempts=5)
def fetch_price_data(ticker):
    # simulate network instability for crypto exchange apis
    if random.random() < 0.7:
        raise ConnectionError('exchange api unreachable')
    return {'ticker': ticker, 'price': random.uniform(20000, 60000)}