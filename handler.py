import math
import logging
from typing import Dict, Any, Union
from decimal import Decimal, InvalidOperation

logger = logging.getLogger("crypto_tracker.handler")

class EdgeCaseAnomaly(Exception):
    """Raised when a crypto payload contains toxic or unparseable market numbers."""
    pass

def sanitize_numeric(value: Any, default: float = 0.0) -> float:
    """Converts strings, None, or odd types to safe floats, handling NaN and flash zeros."""
    if value is None:
        return default
    try:
        if isinstance(value, str):
            cleaned = value.replace("$", "").replace(",", "").strip()
            if cleaned.lower() in ("nan", "inf", "-inf", "null", "none"):
                return default
            val = float(Decimal(cleaned))
        else:
            val = float(value)
        
        if math.isnan(val) or math.isinf(val) or val < 0:
            logger.warning(f"Invalid numeric edge case: {value!r}. Falling back to {default}")
            return default
        return val
    except (ValueError, TypeError, InvalidOperation):
        return default

def safe_ticker_handler(raw_data: Dict[str, Any]) -> Dict[str, Union[str, float]]:
    """Handles weirdly structured or corrupt websocket payloads from crypto exchanges."""
    if not isinstance(raw_data, dict):
        logger.error(f"Malformed payload expected dict, got {type(raw_data).__name__}")
        return {"symbol": "UNKNOWN", "price": 0.0, "volume": 0.0, "spread_ratio": 0.0}

    symbol = str(raw_data.get("symbol") or raw_data.get("pair") or "UNKNOWN").upper().strip()
    price = sanitize_numeric(raw_data.get("price") or raw_data.get("last_price"))
    bid = sanitize_numeric(raw_data.get("bid"))
    ask = sanitize_numeric(raw_data.get("ask"))
    volume = sanitize_numeric(raw_data.get("volume") or raw_data.get("24h_vol"))

    spread_ratio = (ask - bid) / ask if (bid > 0 and ask > 0 and ask >= bid) else 0.0
    if price > 1e9:
        logger.critical(f"Absurd price spike detected for {symbol}: {price}. Clamping data.")
        price = 0.0

    return {
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "spread_ratio": round(spread_ratio, 6)
    }