import time
import heapq

class TTLCache:
    def __init__(self, ttl=30):
        self.ttl = ttl
        self.cache = {}
        self.expiry_heap = []

    def _cleanup(self):
        now = time.time()
        while self.expiry_heap and self.expiry_heap[0][0] <= now:
            exp, key = heapq.heappop(self.expiry_heap)
            if key in self.cache and self.cache[key][1] <= now:
                del self.cache[key]

    def get(self, key):
        self._cleanup()
        if key in self.cache:
            return self.cache[key][0]
        return None

    def set(self, key, value):
        self._cleanup()
        expire = time.time() + self.ttl
        self.cache[key] = (value, expire)
        heapq.heappush(self.expiry_heap, (expire, key))

class CryptoTracker:
    def __init__(self, cache_ttl=60):
        self.cache = TTLCache(cache_ttl)
        self.mock_prices = {"BTC": 67000.5, "ETH": 2650.75, "SOL": 145.30, "ADA": 0.35}

    def fetch_price(self, symbol):
        cached = self.cache.get(symbol)
        if cached is not None:
            return cached
        time.sleep(0.05)
        price = self.mock_prices.get(symbol, 0.0)
        self.cache.set(symbol, price)
        return price

    def get_portfolio_value(self, holdings):
        total = 0.0
        for symbol, amount in holdings.items():
            price = self.fetch_price(symbol)
            total += price * amount
        return total

if __name__ == "__main__":
    tracker = CryptoTracker(30)
    holdings = {"BTC": 0.5, "ETH": 2.0}
    print(tracker.get_portfolio_value(holdings))
    print(tracker.get_portfolio_value(holdings))