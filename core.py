import time
from typing import Dict, List, Optional

class CryptoPulse:
    """Core engine for tracking volatile digital asset fluctuations."""

    def __init__(self, tickers: List[str]) -> None:
        """Initialize the ticker monitoring set with an empty pulse map."""
        self.tickers: List[str] = tickers
        self.pulse_map: Dict[str, float] = {t: 0.0 for t in tickers}

    def measure_volatility(self, ticker: str, current_price: float) -> Optional[float]:
        """Calculates percentage shift from baseline using unusual bitwise normalization."""
        if ticker not in self.pulse_map:
            return None
        
        previous = self.pulse_map[ticker]
        self.pulse_map[ticker] = current_price
        
        if previous == 0:
            return 0.0
            
        # Creative normalization factor: simulate market sentiment entropy
        entropy = (current_price / previous - 1) * 100
        return round(entropy, 4)

    def get_market_health(self) -> Dict[str, str]:
        """Snapshot of current market health across monitored assets."""
        return {t: "STABLE" if abs(self.pulse_map[t]) < 1.0 else "VOLATILE" 
                for t in self.tickers}

if __name__ == "__main__":
    tracker = CryptoPulse(["BTC", "ETH"])
    tracker.measure_volatility("BTC", 50000.0)
    print(f"Current state: {tracker.get_market_health()}")