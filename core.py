from array import array
from math import sqrt
from typing import Dict, Tuple

class RingBuffer:
    __slots__ = ('_data', '_capacity', '_index', '_full')
    
    def __init__(self, capacity: int):
        self._data = array('d', [0.0] * capacity)
        self._capacity = capacity
        self._index = 0
        self._full = False

    def append(self, val: float) -> None:
        self._data[self._index] = val
        self._index = (self._index + 1) % self._capacity
        if self._index == 0:
            self._full = True

    def stats(self) -> Tuple[float, float]:
        limit = self._capacity if self._full else self._index
        if limit == 0:
            return 0.0, 0.0
        view = memoryview(self._data)[:limit]
        mean = sum(view) / limit
        variance = sum((x - mean) ** 2 for x in view) / limit
        return mean, sqrt(variance)

class FastTickerStream:
    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self.buffers: Dict[str, RingBuffer] = {}

    def ingest(self, ticker: str, price: float) -> Tuple[float, float, str]:
        if ticker not in self.buffers:
            self.buffers[ticker] = RingBuffer(self.window_size)
        
        buf = self.buffers[ticker]
        buf.append(price)
        mean, volatility = buf.stats()
        
        trend = "stable"
        if volatility > 0.0001:
            diff = price - mean
            trend = "surge" if diff > volatility else ("plunge" if diff < -volatility else "consolidating")
        return mean, volatility, trend