import re
from typing import Any, Optional

class CryptoValidator:
    def __init__(self):
        self.ticker_pattern = re.compile(r'^[A-Z]{2,6}$')
        self.price_range = (0.00000001, 1_000_000.0)

    def sanitize_input(self, data: Any) -> Optional[dict]:
        try:
            if not isinstance(data, dict):
                return None
            
            ticker = str(data.get('ticker', '')).upper()
            price = float(data.get('price', 0))

            if not self.ticker_pattern.match(ticker):
                return None
            
            if not (self.price_range[0] <= price <= self.price_range[1]):
                return None

            return {'ticker': ticker, 'price': price}
        except (ValueError, TypeError):
            return None

def validate_stream(payload: Any) -> Any:
    validator = CryptoValidator()
    validated = validator.sanitize_input(payload)
    if validated is None:
        raise ValueError(f"Malformed crypto data packet: {payload}")
    return validated

def batch_process(items: list) -> list:
    cleaned = []
    for item in items:
        try:
            cleaned.append(validate_stream(item))
        except ValueError:
            continue
    return cleaned