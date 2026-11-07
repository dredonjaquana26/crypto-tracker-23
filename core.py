import array
import math
from typing import Dict, List, Tuple


class FastTickerBuffer:
    """High-performance pre-allocated ring buffer for raw price tick streams."""
    __slots__ = ('_capacity', '_prices', '_timestamps', '_head', '_count', '_sum')

    def __init__(self, capacity: int = 10000):
        self._capacity = capacity
        self._prices = array.array('d', [0.0] * capacity)
        self._timestamps = array.array('d', [0.0] * capacity)
        self._head = 0
        self._count = 0
        self._sum = 0.0

    def append(self, timestamp: float, price: float) -> None:
        """O(1) tick ingestion maintaining rolling calculations."""
        if self._count == self._capacity:
            self._sum -= self._prices[self._head]
        else:
            self._count += 1

        self._prices[self._head] = price
        self._timestamps[self._head] = timestamp
        self._sum += price
        self._head = (self._head + 1) % self._capacity

    def rolling_sma(self) -> float:
        """Fast arithmetic mean in constant time."""
        if self._count == 0:
            return 0.0
        return self._sum / self._count

    def exp_moving_average(self, period: int = 14) -> float:
        """EMA calculation over pre-allocated ring buffer slice."""
        if self._count == 0:
            return 0.0

        span = min(self._count, period)
        alpha = 2.0 / (span + 1.0)
        start_idx = (self._head - 1) % self._capacity
        ema = self._prices[start_idx]

        for i in range(1, span):
            idx = (self._head - 1 - i) % self._capacity
            ema = (self._prices[idx] * alpha) + (ema * (1.0 - alpha))

        return ema

    def volatility_stddev(self) -> float:
        """Population standard deviation over stored tick window."""
        if self._count <= 1:
            return 0.0

        mean = self._sum / self._count
        variance_sum = 0.0
        prices = self._prices

        for i in range(self._count):
            diff = prices[i] - mean
            variance_sum += diff * diff

        return math.sqrt(variance_sum / self._count)


class CoreMetricsEngine:
    """Optimized execution engine for high-frequency price feeds."""
    def __init__(self, history_depth: int = 5000):
        self._depth = history_depth
        self._symbol_registry: Dict[str, FastTickerBuffer] = {}

    def process_tick_batch(self, batch: List[Tuple[str, float, float]]) -> Dict[str, float]:
        """Process price ticks with localized buffer resolution."""
        registry = self._symbol_registry
        depth = self._depth
        results = {}

        for symbol, ts, price in batch:
            buf = registry.get(symbol)
            if buf is None:
                buf = FastTickerBuffer(depth)
                registry[symbol] = buf

            buf.append(ts, price)
            results[symbol] = buf.rolling_sma()

        return results
