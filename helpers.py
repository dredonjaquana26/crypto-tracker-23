import math
from dataclasses import dataclass
from typing import Callable, Generator, List, Optional


@dataclass(frozen=True)
class Tick:
    symbol: str
    price: float
    volume: float
    timestamp: float


class CryptoPipe:
    """Overloaded pipeline operator for streaming crypto transformations."""

    def __init__(self, func: Callable[[Tick], Optional[dict]]):
        self.func = func

    def __or__(self, other: "CryptoPipe") -> "CryptoPipe":
        def chained(tick: Tick) -> Optional[dict]:
            res = self.func(tick)
            if res is None:
                return None
            return other.func(tick)

        return CryptoPipe(chained)

    def __call__(self, tick: Tick) -> Optional[dict]:
        return self.func(tick)


class AdaptiveAnomalyDetector:
    """Calculates exponential moving average and dynamic z-scores for anomaly detection."""

    def __init__(self, alpha: float = 0.15, threshold: float = 2.5):
        self.alpha = alpha
        self.threshold = threshold
        self.ema: Optional[float] = None
        self.var: float = 0.0

    def process(self, tick: Tick) -> dict:
        price = tick.price
        if self.ema is None:
            self.ema = price
            z_score = 0.0
        else:
            delta = price - self.ema
            self.ema += self.alpha * delta
            self.var = (1 - self.alpha) * (self.var + self.alpha * (delta**2))
            std_dev = math.sqrt(self.var) if self.var > 0 else 1e-6
            z_score = delta / std_dev

        status = "NORMAL"
        if z_score > self.threshold:
            status = "PUMP"
        elif z_score < -self.threshold:
            status = "DUMP"

        return {
            "symbol": tick.symbol,
            "price": round(price, 8),
            "ema": round(self.ema, 8),
            "z_score": round(z_score, 4),
            "status": status,
        }


def analyze_crypto_stream(
    raw_ticks: List[dict], alpha: float = 0.2
) -> Generator[dict, None, None]:
    """Utility function to pipe raw crypto dicts through an adaptive analytical filter."""
    detector = AdaptiveAnomalyDetector(alpha=alpha)
    pipeline = CryptoPipe(lambda t: detector.process(t))

    for raw in raw_ticks:
        tick = Tick(
            symbol=str(raw.get("symbol", "BTC/USD")),
            price=float(raw.get("price", 0.0)),
            volume=float(raw.get("volume", 0.0)),
            timestamp=float(raw.get("ts", 0.0)),
        )
        result = pipeline(tick)
        if result:
            yield result
