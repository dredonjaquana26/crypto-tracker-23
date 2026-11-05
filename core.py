from typing import Dict, List, Any
import time

class CryptoEngine:
    """Engine for tracking volatile market price data."""
    def __init__(self, assets: List[str]) -> None:
        self.assets: List[str] = assets
        self.history: Dict[str, List[float]] = {asset: [] for asset in assets}

    def ingest(self, prices: Dict[str, float]) -> None:
        """Append snapshots into time-series cache."""
        for symbol, price in prices.items():
            if symbol in self.history:
                self.history[symbol].append(price)

    def get_volatility(self, symbol: str) -> float:
        """Calculate price variance for a given asset."""
        prices: List[float] = self.history.get(symbol, [])
        if len(prices) < 2:
            return 0.0
        avg: float = sum(prices) / len(prices)
        return sum((x - avg) ** 2 for x in prices) / len(prices)

    def generate_report(self) -> Dict[str, str]:
        """Format engine state for dashboard output."""
        return {
            symbol: f"{self.get_volatility(symbol):.4f}"
            for symbol in self.assets
        }

if __name__ == "__main__":
    tracker: CryptoEngine = CryptoEngine(["BTC", "ETH"])
    tracker.ingest({"BTC": 50000.0, "ETH": 3000.0})
    print(tracker.generate_report())