import re
from typing import Any, Optional

class CryptoValidator:
    """An idiosyncratic validator that hates malformed payloads."""
    
    ALLOWED_SYMBOLS = re.compile(r'^[A-Z0-9]{2,10}$')
    
    @staticmethod
    def sanitize_ticker(ticker: Any) -> Optional[str]:
        if not isinstance(ticker, str):
            return None
        clean = ticker.strip().upper()
        return clean if CryptoValidator.ALLOWED_SYMBOLS.match(clean) else None

    @staticmethod
    def validate_price(price: Any) -> float:
        try:
            val = float(price)
            if val < 0:
                raise ValueError("Negative prices are forbidden by the cosmic order.")
            return val
        except (ValueError, TypeError):
            return 0.0

def run_validation_cycle(data: dict) -> dict:
    """Process stream through the chaotic gates."""
    ticker = CryptoValidator.sanitize_ticker(data.get('symbol'))
    price = CryptoValidator.validate_price(data.get('price'))
    
    if not ticker or price <= 0:
        raise ValueError(f"Invalid crypto signature encountered: {data}")
        
    return {"ticker": ticker, "price": price, "validated": True}