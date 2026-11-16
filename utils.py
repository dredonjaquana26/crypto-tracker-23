import math
import time
from typing import Dict, Any, Callable, Union


def safe_market_calc(fallback_val: Any = 0.0):
    """Decorator standardizing recovery strategies for crypto calculation anomalies."""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if isinstance(result, (int, float)):
                    if math.isnan(result) or math.isinf(result):
                        return fallback_val
                    if result < 0 and "price" in func.__name__:
                        return fallback_val
                return result
            except (ZeroDivisionError, TypeError, ValueError, OverflowError):
                return fallback_val
        return wrapper
    return decorator


@safe_market_calc(fallback_val=0.0)
def calculate_price_change_pct(current_price: Union[float, str], past_price: Union[float, str]) -> float:
    """Calculate percentage change while handling zero past prices and string inputs."""
    curr = float(current_price)
    past = float(past_price)
    if past == 0.0:
        return 0.0
    return ((curr - past) / past) * 100.0


@safe_market_calc(fallback_val={"status": "corrupt", "price": 0.0, "volume": 0.0, "timestamp": 0})
def normalize_ticker_payload(raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Edge case scrubber for messy DEX/CEX websocket feeds and corrupt ticks."""
    if not isinstance(raw_payload, dict):
        raise ValueError("Payload must be a dictionary")
    
    raw_price = raw_payload.get("price", raw_payload.get("p", 0))
    raw_vol = raw_payload.get("volume", raw_payload.get("v", 0))
    raw_time = raw_payload.get("timestamp", raw_payload.get("t", time.time()))

    price = float(raw_price)
    volume = float(raw_vol)
    timestamp = int(raw_time)
    
    # Handle future timestamp glitches or epoch zero anomalies
    now = int(time.time())
    if timestamp > now + 300 or timestamp < 1500000000:
        timestamp = now
        
    return {
        "symbol": str(raw_payload.get("symbol", raw_payload.get("s", "UNKNOWN"))).upper(),
        "price": abs(price),
        "volume": abs(volume),
        "timestamp": timestamp,
        "status": "valid"
    }
