import functools
import time

CACHE_TTL = 60
_memo_store = {}

def memoize_with_expiry(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (func.__name__, args, frozenset(kwargs.items()))
        now = time.monotonic()
        if key in _memo_store:
            val, timestamp = _memo_store[key]
            if now - timestamp < CACHE_TTL:
                return val
        result = func(*args, **kwargs)
        _memo_store[key] = (result, now)
        return result
    return wrapper

class DataStreamOptimizer:
    @staticmethod
    def batch_process(data_stream, chunk_size=100):
        it = iter(data_stream)
        while True:
            chunk = []
            try:
                for _ in range(chunk_size):
                    chunk.append(next(it))
                yield chunk
            except StopIteration:
                if chunk:
                    yield chunk
                break

    @staticmethod
    def fast_float_map(iterable):
        return map(float, iterable)

def sanitize_tick_data(data):
    return [d for d in data if d.get('price', 0) > 0]