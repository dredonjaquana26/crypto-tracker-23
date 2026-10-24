from typing import Dict, List, Any
from datetime import datetime

class CryptoTransformer:
    """Utility class for transforming raw crypto exchange payloads."""
    def __init__(self, currency_map: Dict[str, str]):
        self.currency_map = currency_map

    def sanitize_ticker(self, ticker: str) -> str:
        return self.currency_map.get(ticker.upper(), ticker)

    def process_batch(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                "symbol": self.sanitize_ticker(d.get("s", "UNKNOWN")),
                "price": float(d.get("p", 0.0)),
                "timestamp": datetime.fromtimestamp(d.get("t", 0) / 1000).isoformat(),
                "source": "crypto-tracker-23"
            }
            for d in raw_data
            if "p" in d
        ]

def calculate_volatility(prices: List[float]) -> float:
    """Calculate basic price variance for crypto assets."""
    if len(prices) < 2:
        return 0.0
    mean = sum(prices) / len(prices)
    variance = sum((x - mean) ** 2 for x in prices) / len(prices)
    return variance ** 0.5

def format_crypto_amount(value: float, precision: int = 8) -> str:
    """Custom formatter for crypto precision handling."""
    template = "{:.%df}" % precision
    return template.format(value).rstrip('0').rstrip('.') or '0'