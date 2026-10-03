import time
import functools
import logging

logger = logging.getLogger('crypto-tracker-23')

class CryptoCircuitBreaker:
    def __init__(self, retries=3, delay=1.0):
        self.retries = retries
        self.delay = delay

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f"Retry {attempt+1}/{self.retries} after {e}")
                    time.sleep(self.delay * (2 ** attempt))
            logger.error("Circuit broken: maximum retries reached")
            raise last_ex
        return wrapper

@CryptoCircuitBreaker(retries=3, delay=0.5)
def fetch_price_safely(symbol, api_client):
    if not symbol or not isinstance(symbol, str):
        raise ValueError(f"Invalid symbol format: {symbol}")
    
    response = api_client.get(f"/v1/ticker/{symbol.upper()}")
    if response.status_code == 429:
        raise ConnectionError("Rate limit exceeded")
    
    return response.json().get('price', 0.0)

def sanitize_response(data, fallback=0.0):
    try:
        return float(data) if data is not None else fallback
    except (ValueError, TypeError):
        return fallback