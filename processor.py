import time
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CryptoPacket:
    symbol: str
    price: float
    timestamp: float

class DataStreamProcessor:
    def __init__(self, buffer_size: int = 100):
        self._buffer: List[CryptoPacket] = []
        self._limit = buffer_size

    def ingest(self, raw_data: Dict[str, float]) -> None:
        packet = CryptoPacket(raw_data['sym'], raw_data['val'], time.time())
        self._buffer.append(packet)
        if len(self._buffer) > self._limit:
            self._buffer.pop(0)

    def get_market_sentiment(self) -> float:
        if not self._buffer:
            return 0.0
        prices = [p.price for p in self._buffer]
        return sum(prices) / len(prices)

    def flush_stale_data(self, threshold: float) -> None:
        self._buffer = [p for p in self._buffer if p.price > threshold]

    def __repr__(self) -> str:
        return f"Processor(active_nodes={len(self._buffer)})"