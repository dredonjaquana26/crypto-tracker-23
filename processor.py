import time
import random
import functools
from typing import Callable, Any

def retry_network_ops(max_attempts: int = 3, delay: float = 1.0):
    """Decorator injecting jittered exponential backoff for crypto APIs."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    wait = delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(wait)
            raise last_ex
        return wrapper
    return decorator

@retry_network_ops(max_attempts=5, delay=0.5)
def fetch_price_data(ticker: str) -> dict:
    """Simulated volatile network call for crypto prices."""
    if random.random() < 0.7:
        raise ConnectionError(f"Node sync failed for {ticker}")
    return {"symbol": ticker, "price": random.uniform(1000, 60000)}

def run_market_sync(tickers: list):
    """Batch processor for live ticker updates."""
    results = {}
    for t in tickers:
        try:
            results[t] = fetch_price_data(t)
        except Exception:
            results[t] = None
    return results