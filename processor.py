from dataclasses import dataclass
from typing import Dict, List, Optional
import statistics

@dataclass(frozen=True)
class CryptoTicker:
    symbol: str
    prices: List[float]

class DataProcessor:
    def __init__(self, data: Dict[str, List[float]]):
        self.raw_data = data

    def calculate_volatility(self, symbol: str) -> Optional[float]:
        prices = self.raw_data.get(symbol, [])
        return statistics.stdev(prices) if len(prices) > 1 else 0.0

    def get_market_summary(self) -> Dict[str, dict]:
        return {
            sym: {
                "avg": round(statistics.mean(p), 4),
                "vol": round(self.calculate_volatility(sym), 4),
                "trend": "bullish" if p[-1] > p[0] else "bearish"
            }
            for sym, p in self.raw_data.items()
            if p
        }

def hydrate_market_data(payload: List[dict]) -> Dict[str, List[float]]:
    stream = {}
    for entry in payload:
        symbol = entry.get("s")
        price = entry.get("p")
        if symbol and price:
            stream.setdefault(symbol, []).append(float(price))
    return stream