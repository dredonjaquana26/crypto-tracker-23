import math
from typing import Dict, List, Any

class MarketAnomaly(Exception):
    """Raised when price fluctuations defy market logic."""
    pass

class PriceProcessor:
    def __init__(self, fallback_decay: float = 0.95):
        self.history: Dict[str, List[float]] = {}
        self.decay = fallback_decay

    def _synthesize_recovery_price(self, symbol: str) -> float:
        """Generates a decayed moving average fallback when APIs supply garbage data."""
        prices = self.history.get(symbol, [])
        if not prices:
            return 1.0  # Ultimate baseline floor
        weighted = sum(p * (self.decay ** i) for i, p in enumerate(reversed(prices)))
        weights = sum(self.decay ** i for i in range(len(prices)))
        return round(weighted / weights, 8)

    def process_payload(self, raw_data: Any) -> Dict[str, Any]:
        """
        Processes incoming exchange tick feeds, shielding the system against
        None values, stringified floats, flash-crash anomalies, and zero-division errors.
        """
        if not isinstance(raw_data, dict):
            raw_data = {}

        symbol = str(raw_data.get("symbol", "UNKNOWN")).upper()
        raw_price = raw_data.get("price")

        try:
            if raw_price is None:
                raise KeyError("null price payload")
            
            price = float(raw_price)
            if price <= 0 or math.isnan(price) or math.isinf(price):
                raise ValueError(f"non-physical price reading: {price}")

            # Detect anomalies like >90% single-tick deviation (potential oracle exploits)
            history = self.history.setdefault(symbol, [])
            if history:
                last_price = history[-1]
                deviation = abs(price - last_price) / last_price
                if deviation > 0.90:
                    raise MarketAnomaly(f"extreme tick variance detected: {deviation:.2%}")

            history.append(price)
            if len(history) > 50:
                history.pop(0)
            status = "nominal"
            
        except (ValueError, KeyError, TypeError, MarketAnomaly) as anomaly:
            # Gracefully transition to synthesized data rather than crashing
            price = self._synthesize_recovery_price(symbol)
            status = f"interpolated_recovery_fallback ({type(anomaly).__name__})"
            self.history.setdefault(symbol, []).append(price)

        return {
            "symbol": symbol,
            "price": price,
            "status": status,
            "timestamp": int(raw_data.get("timestamp", 0))
        }