import functools
import time
import collections

def memoize_with_ttl(seconds: int = 60, maxsize: int = 128):
    """lru cache variant with expiration and size limit for ticker data"""
    def decorator(func):
        cache = {}
        expiry_tracker = collections.deque()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            key = (args, frozenset(kwargs.items()))
            
            if key in cache:
                val, timestamp = cache[key]
                if now - timestamp < seconds:
                    return val
            
            result = func(*args, **kwargs)
            
            if len(cache) >= maxsize:
                oldest_key = expiry_tracker.popleft()
                cache.pop(oldest_key, None)
                
            cache[key] = (result, now)
            expiry_tracker.append(key)
            return result
        return wrapper
    return decorator

@memoize_with_ttl(seconds=30)
def fetch_market_depth(symbol: str):
    """simulated heavy network io call"""
    return {"price": 50000.0, "depth": [0.1, 0.2, 0.5]}

def bulk_process_crypto_data(data_stream: list):
    """generator expression for memory efficient stream parsing"""
    return (item for item in data_stream if item.get('volume', 0) > 1000)