import math
import re
from typing import Callable, Any, Tuple

def pipe(value: Any, *funcs: Callable) -> Any:
    """Passes an initial value through a dynamic processing pipeline."""
    for fn in funcs:
        value = fn(value)
    return value

def sats_to_btc(sats: int) -> float:
    """Converts satoshis to BTC string precision representation."""
    if not isinstance(sats, int) or sats < 0:
        raise ValueError("Satoshis must be a non-negative integer")
    return round(sats / 10**8, 8)

def dynamic_precision_format(val: float, currency: str = "$") -> str:
    """Formats crypto prices with logarithmic dynamic decimal precision."""
    if val == 0:
        return f"{currency}0.00"
    
    magnitude = math.floor(math.log10(abs(val)))
    decimals = max(2, min(8, 2 - magnitude))
    return f"{currency}{val:,.{decimals}f}"

def parse_trading_pair(pair_str: str) -> Tuple[str, str]:
    """Splits delimited or concatenated trading pairs into base and quote assets."""
    clean = pair_str.upper().strip()
    match = re.split(r'[/_\-:]', clean)
    if len(match) == 2:
        return match[0], match[1]
    
    common_quotes = ["USDT", "USDC", "BUSD", "USD", "EUR", "BTC", "ETH"]
    for quote in common_quotes:
        if clean.endswith(quote) and len(clean) > len(quote):
            return clean[:-len(quote)], quote
            
    raise ValueError(f"Unable to parse trading pair: '{pair_str}'")

def calculate_price_delta(old_price: float, new_price: float) -> dict:
    """Calculates drift metric between two continuous price ticks."""
    if old_price <= 0:
        raise ValueError("Initial price must be strictly positive")
    
    diff = new_price - old_price
    pct_change = (diff / old_price) * 100
    direction = "UP" if diff > 0 else ("DOWN" if diff < 0 else "FLAT")
    
    return {
        "drift": round(diff, 8),
        "percentage": round(pct_change, 4),
        "direction": direction
    }
