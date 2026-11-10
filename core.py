import array
from typing import Dict, List, Tuple


class FastTickRingBuffer:
    """High-performance fixed-capacity ring buffer using typed native arrays."""
    __slots__ = ('_capacity', '_prices', '_timestamps', '_head', '_count', '_sum')

    def __init__(self, capacity: int = 1000):
        self._capacity = capacity
        self._prices = array.array('d', [0.0] * capacity)
        self._timestamps = array.array('d', [0.0] * capacity)
        self._head = 0
        self._count = 0
        self._sum = 0.0

    def push(self, timestamp: float, price: float) -> None:
        if self._count < self._capacity:
            idx = self._count
            self._count += 1
        else:
            idx = self._head
            self._sum -= self._prices[idx]
            self._head = (self._head + 1) % self._capacity

        self._timestamps[idx] = timestamp
        self._prices[idx] = price
        self._sum += price

    def moving_average(self) -> float:
        return self._sum / self._count if self._count > 0 else 0.0


class CryptoCoreTracker:
    """Optimized core ticker processing engine using aligned memory buffers."""
    __slots__ = ('_buffers', '_window_size')

    def __init__(self, window_size: int = 500):
        self._window_size = window_size
        self._buffers: Dict[str, FastTickRingBuffer] = {}

    def ingest_ticks(self, batch: List[Tuple[str, float, float]]) -> Dict[str, float]:
        results = {}
        for symbol, timestamp, price in batch:
            if symbol not in self._buffers:
                self._buffers[symbol] = FastTickRingBuffer(self._window_size)
            buf = self._buffers[symbol]
            buf.push(timestamp, price)
            results[symbol] = buf.moving_average()
        return results

    def get_volatility(self, symbol: str) -> float:
        buf = self._buffers.get(symbol)
        if not buf or buf._count < 2:
            return 0.0
        mean = buf.moving_average()
        variance = sum((buf._prices[i] - mean) ** 2 for i in range(buf._count)) / buf._count
        return variance ** 0.5
