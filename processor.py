from decimal import Decimal
from datetime import datetime
from typing import Union, List

def sanitize_price(val: Union[str, float, int]) -> Decimal:
    return Decimal(str(val)).quantize(Decimal('0.00000001'))

def format_timestamp(ts: Union[int, float]) -> str:
    return datetime.fromtimestamp(ts).isoformat()

def batch_normalize(data: List[dict], key: str) -> List[Decimal]:
    return [sanitize_price(item[key]) for item in data if key in item]

def volatility_score(prices: List[Decimal]) -> Decimal:
    if len(prices) < 2:
        return Decimal('0')
    spread = max(prices) - min(prices)
    return (spread / max(prices)) * 100

def generate_ticker_slug(base: str, quote: str) -> str:
    return f"{base.upper()}_{quote.upper()}"

def partition_stream(items: List[dict], chunk_size: int = 10):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def calculate_roi(initial: Decimal, current: Decimal) -> Decimal:
    if initial == 0:
        return Decimal('0')
    return ((current - initial) / initial) * 100