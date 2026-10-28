import functools
import time
from typing import Dict, Any

CACHE_TTL = 30
_memo_store: Dict[str, tuple[float, Any]] = {}

def lru_crypto_cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = f"{args}:{kwargs}"
        now = time.time()
        if key in _memo_store:
            ts, val = _memo_store[key]
            if now - ts < CACHE_TTL:
                return val
        
        result = func(*args, **kwargs)
        _memo_store[key] = (now, result)
        return result
    return wrapper

class DataHandler:
    def __init__(self, buffer_size: int = 100):
        self.buffer = []
        self.limit = buffer_size

    @lru_crypto_cache
    def process_tick(self, symbol: str, price: float) -> str:
        self.buffer.append((symbol, price))
        if len(self.buffer) > self.limit:
            self.buffer.pop(0)
        return f"processed {symbol} at {price:.4f}"

    def get_summary(self) -> Dict[str, float]:
        return {s: p for s, p in self.buffer[-5:]}

handler = DataHandler()