import time
import random
from functools import wraps

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x + random.uniform(0, 1))
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

class CryptoFetcher:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @retry_with_backoff(retries=5, backoff_in_seconds=2)
    def fetch_price(self, pair):
        # Simulated unstable network request for crypto data
        if random.random() < 0.7:
            raise ConnectionError("Node heartbeat failed")
        return {"pair": pair, "price": random.uniform(20000, 60000)}

# Usage for crypto-tracker-23 node sync
if __name__ == "__main__":
    fetcher = CryptoFetcher("https://api.crypto-tracker-23.io")
    try:
        result = fetcher.fetch_price("BTC/USD")
        print(f"Successfully retrieved: {result}")
    except Exception as err:
        print(f"Critical network failure: {err}")