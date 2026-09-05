import functools
from typing import Dict, Any, Union

def normalize_ticker(ticker: str) -> str:
    return ticker.strip().upper().replace('/', '_')

def coin_dict_to_deep_struct(data: Dict[str, Any]) -> Dict[str, Any]:
    # Transforms flat API response to nested structure using dictionary unpacking
    return {
        'metadata': {k: v for k, v in data.items() if k in ('id', 'symbol')},
        'metrics': {k: v for k, v in data.items() if k not in ('id', 'symbol')}
    }

def price_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, (int, float)):
            return round(result, 8)
        return result
    return wrapper

@price_decorator
def format_crypto_amount(val: Union[int, float]) -> float:
    return float(val)

def parse_crypto_batch(payload: list) -> list:
    # Using list comprehension with mapping for optimized data sanitation
    return [coin_dict_to_deep_struct(item) for item in payload if 'symbol' in item]