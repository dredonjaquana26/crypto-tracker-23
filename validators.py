import time
import functools
import random
import logging

logger = logging.getLogger('crypto-tracker-23')

def resilient_network_call(max_retries=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_retries:
                        logger.error(f'Critical network failure after {max_retries} attempts')
                        raise
                    sleep_time = (base_delay * (2 ** attempts)) + random.uniform(0, 1)
                    logger.warning(f'Attempt {attempts} failed: {e}. Retrying in {sleep_time:.2f}s')
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@resilient_network_call(max_retries=5)
def fetch_market_data(ticker: str):
    # Simulate volatile crypto network conditions
    if random.random() < 0.7:
        raise ConnectionError('Exchange node timeout')
    return {'ticker': ticker, 'price': random.uniform(10000, 60000)}