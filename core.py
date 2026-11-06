import array
import math
from typing import Tuple


class FastTickWindow:
    """
    High-performance circular memory buffer for continuous VWAP and price analytics.
    Eliminates GC pressure by pre-allocating contiguous C-arrays for tick streams.
    """

    __slots__ = (
        "_prices",
        "_volumes",
        "_capacity",
        "_head",
        "_size",
        "_sum_pv",
        "_sum_v",
    )

    def __init__(self, capacity: int = 10_000):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._prices = array.array("d", [0.0] * capacity)
        self._volumes = array.array("d", [0.0] * capacity)
        self._head = 0
        self._size = 0
        self._sum_pv = 0.0
        self._sum_v = 0.0

    def push(self, price: float, volume: float) -> None:
        """Pushes a new tick into the circular buffer with O(1) state updates."""
        if self._size == self._capacity:
            old_p = self._prices[self._head]
            old_v = self._volumes[self._head]
            self._sum_pv -= old_p * old_v
            self._sum_v -= old_v
        else:
            self._size += 1

        pv = price * volume
        self._prices[self._head] = price
        self._volumes[self._head] = volume
        self._sum_pv += pv
        self._sum_v += volume

        self._head = (self._head + 1) % self._capacity

    def vwap(self) -> float:
        """Calculates current Volume Weighted Average Price in O(1) time."""
        if self._sum_v == 0.0:
            return 0.0
        return self._sum_pv / self._sum_v

    def volatility(self) -> float:
        """Fast standard deviation calculation over buffered prices."""
        if self._size < 2:
            return 0.0
        mean = sum(self._prices[: self._size]) / self._size
        variance = sum((p - mean) ** 2 for p in self._prices[: self._size]) / (
            self._size - 1
        )
        return math.sqrt(variance)

    def snapshot(self) -> Tuple[float, float, int]:
        """Returns (VWAP, standard_deviation, window_length)."""
        return self.vwap(), self.volatility(), self._size
