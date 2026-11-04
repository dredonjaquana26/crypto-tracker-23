import decimal
from functools import wraps
from typing import Any, Callable, Dict, Union

def sanitize_price(value: Union[str, float, int]) -> decimal.Decimal:
    try:
        return decimal.Decimal(str(value)).quantize(decimal.Decimal('0.00000001'))
    except Exception:
        return decimal.Decimal('0.0')

def memoize_crypto_data(ttl: int = 60):
    cache = {}
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            key = str(args) + str(kwargs)
            now = time.time()
            if key in cache and (now - cache[key]['ts'] < ttl):
                return cache[key]['data']
            result = func(*args, **kwargs)
            cache[key] = {'data': result, 'ts': now}
            return result
        return wrapper
    return decorator

def calculate_delta(initial: float, current: float) -> float:
    if initial == 0:
        return 0.0
    return ((current - initial) / initial) * 100

def format_ticker(symbol: str, pair: str = 'USD') -> str:
    clean = ''.join(filter(str.isalnum, symbol)).upper()
    return f"{clean}/{pair.upper()}"

class DataPipeline:
    def __init__(self):
        self.steps = []

    def pipe(self, func: Callable):
        self.steps.append(func)
        return self

    def execute(self, data: Any) -> Any:
        for step in self.steps:
            data = step(data)
        return data