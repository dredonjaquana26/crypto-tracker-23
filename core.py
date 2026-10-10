import time
import random
import functools
import requests

def resilient_network_call(max_retries=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.RequestException, ConnectionError) as e:
                    last_exception = e
                    sleep_time = (base_delay * (2 ** attempt)) + (random.random() * 0.5)
                    time.sleep(sleep_time)
            raise last_exception
        return wrapper
    return decorator

@resilient_network_call(max_retries=5)
def fetch_crypto_price(ticker):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ticker}&vs_currencies=usd"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    return data.get(ticker, {}).get('usd')

if __name__ == "__main__":
    price = fetch_crypto_price('bitcoin')
    print(f"Current BTC price: ${price}")