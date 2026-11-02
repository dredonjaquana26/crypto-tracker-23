from typing import Any, Dict, Union

class CryptoDataError(Exception):
    pass

def validate_ticker(ticker: Any) -> str:
    if not isinstance(ticker, str) or not ticker.isupper() or len(ticker) not in range(2, 6):
        raise CryptoDataError(f"invalid ticker format: {ticker}")
    return ticker

def sanitize_price(price: Any) -> float:
    try:
        value = float(price)
        if value < 0:
            raise ValueError
        return value
    except (ValueError, TypeError):
        raise CryptoDataError(f"invalid price point detected: {price}")

def process_payload(data: Dict[str, Any]) -> Dict[str, Union[str, float]]:
    required = {'symbol': validate_ticker, 'price': sanitize_price}
    processed = {}
    for key, validator in required.items():
        if key not in data:
            raise CryptoDataError(f"missing required key: {key}")
        processed[key] = validator(data[key])
    return processed

def input_loop_guard(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CryptoDataError as e:
            return {'status': 'rejected', 'reason': str(e)}
    return wrapper