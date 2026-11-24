import functools
from typing import Any, Callable, Dict

def sanitize_price(value: Any) -> float:
    try:
        return float(str(value).replace(',', ''))
    except (ValueError, TypeError):
        return 0.0

def memoize_crypto_data(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

@memoize_crypto_data
def format_ticker(symbol: str, exchange: str = 'binance') -> str:
    return f"{symbol.upper()}:{exchange.lower()}"

def normalize_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "pair": format_ticker(data.get('s', 'BTC'), data.get('e', 'default')),
        "price": sanitize_price(data.get('p', 0)),
        "ts": int(data.get('t', 0)) // 1000
    }

def batch_process(items: list, chunk_size: int = 10) -> list:
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]