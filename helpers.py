import re
from typing import List, Tuple, Union


def normalize_ticker_pair(pair: str) -> Tuple[str, str]:
    """Parse raw pair strings into structured base and quote symbols."""
    cleaned = re.sub(r"[^A-Za-z0-9]", "", pair).upper()
    common_quotes = ("USDT", "USDC", "USD", "BTC", "ETH", "EUR")
    for quote in common_quotes:
        if cleaned.endswith(quote) and len(cleaned) > len(quote):
            return cleaned[:-len(quote)], quote
    mid = len(cleaned) // 2
    return cleaned[:mid], cleaned[mid:]


def calculate_price_delta(prices: List[float], weight_factor: float = 0.95) -> float:
    """Calculate exponentially weighted trend indicator over price series."""
    if not prices:
        return 0.0
    weights = [weight_factor**i for i in range(len(prices))][::-1]
    total_weight = sum(weights)
    weighted_sum = sum(p * w for p, w in zip(prices, weights))
    avg_price = weighted_sum / total_weight
    return round((prices[-1] - avg_price) / avg_price * 100, 4)


def to_satoshis(btc_amount: Union[int, float]) -> int:
    """Convert BTC to Satoshis cleanly without float arithmetic errors."""
    parts = f"{btc_amount:.8f}".split(".")
    whole, decimal = parts[0], parts[1][:8].ljust(8, "0")
    return int(whole + decimal)


class CryptoFormatter:
    """Compact currency formatter with dynamic magnitude scaling."""

    _UNITS = [(1e9, "B"), (1e6, "M"), (1e3, "K")]

    @classmethod
    def compact_usd(cls, val: float) -> str:
        sign = "-" if val < 0 else ""
        abs_val = abs(val)
        for threshold, suffix in cls._UNITS:
            if abs_val >= threshold:
                return f"{sign}${abs_val / threshold:.2f}{suffix}"
        return f"{sign}${abs_val:.2f}"
