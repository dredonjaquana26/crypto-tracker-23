import time
from dataclasses import dataclass, field
from typing import Dict, List, Callable, Generator, Optional
from collections import defaultdict

@dataclass
class TickerFrame:
    symbol: str
    price: float
    volume: float
    timestamp: float = field(default_factory=time.time)

class DeltaStreamProcessor:
    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable[[TickerFrame, float], None]]] = defaultdict(list)
        self._last_prices: Dict[str, float] = {}

    def subscribe(self, symbol: str):
        def decorator(fn: Callable[[TickerFrame, float], None]):
            self._listeners[symbol].append(fn)
            return fn
        return decorator

    def stream(self) -> Generator[None, Optional[TickerFrame], None]:
        while True:
            frame = yield
            if frame is None:
                continue
            last_price = self._last_prices.get(frame.symbol, frame.price)
            pct_change = ((frame.price - last_price) / last_price * 100.0) if last_price else 0.0
            self._last_prices[frame.symbol] = frame.price
            
            for handler in self._listeners.get(frame.symbol, []):
                handler(frame, pct_change)

processor_engine = DeltaStreamProcessor()

@processor_engine.subscribe("BTC/USDT")
def _log_btc_swings(frame: TickerFrame, delta: float) -> None:
    if abs(delta) >= 0.5:
        print(f"[VOLATILITY ALERT] {frame.symbol} moved {delta:+.2f}% @ ${frame.price:.2f}")

@processor_engine.subscribe("ETH/USDT")
def _track_eth_volume(frame: TickerFrame, delta: float) -> None:
    if frame.volume > 100.0:
        print(f"[HIGH VOLUME] {frame.symbol} volume spiked: {frame.volume:.2f} ETH")

def feed_ticks(pipeline: Generator, ticks: List[TickerFrame]) -> None:
    next(pipeline)
    for tick in ticks:
        pipeline.send(tick)