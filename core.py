import array
import math
from typing import Tuple, Dict, Any


class FastTickerBuffer:
    """High-performance circular buffer for streaming crypto tick data using fixed-size array allocations."""

    __slots__ = ('_capacity', '_prices', '_head', '_count', '_sum')

    def __init__(self, capacity: int = 1000):
        self._capacity = capacity
        self._prices = array.array('d', [0.0] * capacity)
        self._head = 0
        self._count = 0
        self._sum = 0.0

    def push(self, price: float) -> None:
        """Push a new price tick into the buffer with O(1) rolling sum update."""
        if self._count == self._capacity:
            self._sum -= self._prices[self._head]
        else:
            self._count += 1

        self._prices[self._head] = price
        self._sum += price
        self._head = (self._head + 1) % self._capacity

    def stats(self) -> Tuple[float, float, float, float]:
        """Compute mean, volatility (std dev), min, and max without allocating new lists."""
        if self._count == 0:
            return 0.0, 0.0, 0.0, 0.0

        mean = self._sum / self._count
        variance_sum = 0.0
        min_val = float('inf')
        max_val = float('-inf')

        for i in range(self._count):
            p = self._prices[i]
            diff = p - mean
            variance_sum += diff * diff
            if p < min_val:
                min_val = p
            if p > max_val:
                max_val = p

        std_dev = math.sqrt(variance_sum / self._count)
        return mean, std_dev, min_val, max_val


class CryptoCorePipeline:
    """Core high-throughput signal pipeline for processing raw ticker streams."""

    def __init__(self, buffer_size: int = 5000):
        self.tickers: Dict[str, FastTickerBuffer] = {}
        self.buffer_size = buffer_size

    def process_tick(self, symbol: str, price: float) -> Dict[str, Any]:
        if symbol not in self.tickers:
            self.tickers[symbol] = FastTickerBuffer(self.buffer_size)

        buf = self.tickers[symbol]
        buf.push(price)
        mean, std, min_p, max_p = buf.stats()

        z_score = (price - mean) / std if std > 1e-9 else 0.0

        return {
            "symbol": symbol,
            "latest": price,
            "sma": mean,
            "volatility": std,
            "z_score": z_score,
            "range": (min_p, max_p)
        }
