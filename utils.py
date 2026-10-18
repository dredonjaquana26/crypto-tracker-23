import functools
import time
import collections

class memoize_with_expiry:
    def __init__(self, ttl_seconds):
        self.ttl = ttl_seconds
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def batch_process(items, batch_size=50):
    """Chunking logic for massive ticker updates."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

@memoize_with_expiry(ttl_seconds=30)
def fetch_market_rate(ticker):
    """Simulated expensive API network call."""
    print(f"Fetching fresh data for {ticker}...")
    return 42000.69

class StreamProcessor:
    def __init__(self):
        self.queue = collections.deque(maxlen=1000)

    def ingest(self, data_packet):
        self.queue.append(data_packet)

    def get_batch_summary(self):
        return list(self.queue)