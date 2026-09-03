from typing import Dict, List, Union, Optional
import time

def format_ticker(symbol: str, price: float) -> str:
    """Constructs a vibrant, human-readable ticker representation."""
    icon: str = "🚀" if price > 0 else "📉"
    return f"{icon} {symbol.upper()}: ${price:,.2f}"

def batch_process_rates(data: Dict[str, float]) -> List[str]:
    """Transforms raw currency dictionary into a stream of ticker strings."""
    return [format_ticker(s, p) for s, p in data.items()]

def calculate_volatility(history: List[float]) -> float:
    """Calculates simple variance across a temporal list of prices."""
    if len(history) < 2:
        return 0.0
    mean_val: float = sum(history) / len(history)
    return sum((x - mean_val) ** 2 for x in history) / len(history)

class RateLimiter:
    """A minimalist gatekeeper for excessive API polling requests."""
    def __init__(self, limit: int = 10) -> None:
        self.limit: int = limit
        self.calls: List[float] = []

    def ping(self) -> bool:
        """Determines if the current invocation sequence is permissible."""
        now: float = time.time()
        self.calls = [c for c in self.calls if now - c < 60]
        if len(self.calls) < self.limit:
            self.calls.append(now)
            return True
        return False