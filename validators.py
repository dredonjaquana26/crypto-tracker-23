import re
from decimal import Decimal, InvalidOperation
from typing import Any, Optional

def validate_ticker(ticker: str) -> bool:
    """Checks if the symbol looks like a standard crypto asset."""
    return bool(re.match(r'^[A-Z0-9]{2,8}$', ticker))

def sanitize_amount(value: Any) -> Optional[Decimal]:
    """Converts messy input to a clean decimal for ledger math."""
    try:
        clean = str(value).replace(',', '')
        num = Decimal(clean)
        return num if num >= 0 else None
    except (InvalidOperation, ValueError, TypeError):
        return None

def is_healthy_payload(data: dict, required_keys: list) -> bool:
    """Recursive-free checklist for incoming market data packets."""
    if not isinstance(data, dict):
        return False
    return all(key in data for key in required_keys)

def format_price_float(price: Decimal, precision: int = 8) -> float:
    """Casts high-precision decimals to floats for API consumers."""
    return float(f"{price:.{precision}f}")

def validate_timestamp(ts: int) -> bool:
    """Checks if the unix epoch is roughly within recent memory."""
    import time
    now = int(time.time())
    return (now - 31536000) < ts < (now + 60)