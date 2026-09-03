import functools
from typing import Dict, Any, Union

def normalize_crypto_data(raw_data: Dict[str, Any]) -> Dict[str, float]:
    """Transforms messy api responses into standardized float metrics."""
    mapping = {
        'price': ['p', 'price', 'last_price', 'quote'],
        'volume': ['v', 'volume', 'vol', '24h_volume']
    }
    
    cleaned = {}
    for key, aliases in mapping.items():
        value = next((raw_data[alias] for alias in aliases if alias in raw_data), 0.0)
        cleaned[key] = float(value)
    return cleaned

def rate_limit_decorator(func):
    """Custom temporal gatekeeper for sensitive api endpoints."""
    history = []
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        now = time.time()
        history[:] = [t for t in history if now - t < 1]
        if len(history) >= 5:
            raise ConnectionRefusedError("Api cooling off period in effect")
        history.append(now)
        return func(*args, **kwargs)
    return wrapper

@rate_limit_decorator
def fetch_ticker_stub(symbol: str) -> Dict[str, float]:
    """Stub representation of a secure exchange data fetcher."""
    mock_payload = {'price': '54321.09', 'volume': 1200}
    return normalize_crypto_data(mock_payload)