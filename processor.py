import math
from decimal import Decimal
from datetime import datetime

def normalize_crypto_asset(asset_string: str) -> str:
    return asset_string.strip().upper().replace(' ', '_')

def calculate_volatility(prices: list[float], window: int = 5) -> float:
    if len(prices) < window:
        return 0.0
    slice_prices = prices[-window:]
    mean = sum(slice_prices) / len(slice_prices)
    variance = sum((x - mean) ** 2 for x in slice_prices) / len(slice_prices)
    return math.sqrt(variance)

def format_price_impact(base: str, target: str, diff: float) -> str:
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    indicator = '▲' if diff >= 0 else '▼'
    formatted_diff = f"{abs(diff):.4f}%"
    return f"[{timestamp}] {base}/{target} shift: {indicator}{formatted_diff}"

def sanitize_trade_amount(raw_val: str | float) -> Decimal:
    try:
        return Decimal(str(raw_val)).quantize(Decimal('0.00000001'))
    except Exception:
        return Decimal('0.00000000')

def batch_process_ticks(ticks: list[dict], threshold: float) -> list[dict]:
    return [t for t in ticks if abs(t.get('change', 0)) > threshold]
