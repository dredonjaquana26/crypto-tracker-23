import time
import functools
import random

def retry_operation(max_attempts=3, backoff=2):
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
                        raise e
                    sleep_time = (backoff ** attempts) + random.uniform(0, 1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_operation(max_attempts=5, backoff=1.5)
def fetch_crypto_price(ticker):
    # Simulate network instability in crypto API calls
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach market node for {ticker}")
    return {"ticker": ticker, "price": round(random.uniform(1000, 60000), 2)}