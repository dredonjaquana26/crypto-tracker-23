from array import array
from typing import Dict, Optional

class FastTickerStream:
    """High-throughput sliding window ticker aggregator using fixed-point integer arrays."""
    
    __slots__ = ('_capacity', '_scale', '_buffers', '_pointers', '_counts')

    def __init__(self, capacity: int = 1024, decimal_precision: int = 4):
        self._capacity = capacity
        self._scale = 10 ** decimal_precision
        self._buffers: Dict[str, array] = {}
        self._pointers: Dict[str, int] = {}
        self._counts: Dict[str, int] = {}

    def register_symbol(self, symbol: str) -> None:
        if symbol not in self._buffers:
            self._buffers[symbol] = array('q', [0] * self._capacity)
            self._pointers[symbol] = 0
            self._counts[symbol] = 0

    def push_price(self, symbol: str, price: float) -> None:
        if symbol not in self._buffers:
            self.register_symbol(symbol)

        scaled_val = int(price * self._scale)
        idx = self._pointers[symbol]
        self._buffers[symbol][idx] = scaled_val
        
        self._pointers[symbol] = (idx + 1) % self._capacity
        if self._counts[symbol] < self._capacity:
            self._counts[symbol] += 1

    def get_moving_average(self, symbol: str, window: Optional[int] = None) -> float:
        if symbol not in self._buffers or self._counts[symbol] == 0:
            return 0.0

        count = min(window or self._counts[symbol], self._counts[symbol])
        buf = self._buffers[symbol]
        head = self._pointers[symbol]
        
        mv = memoryview(buf)
        if head >= count:
            total = sum(mv[head - count : head])
        else:
            total = sum(mv[self._capacity - (count - head) : self._capacity]) + sum(mv[:head])

        return (total / count) / self._scale