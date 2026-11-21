import re

class CryptoValidator:
    """An unorthodox set of validation gates for crypto assets."""

    SYMBOL_PATTERN = re.compile(r'^[A-Z]{2,6}$')

    @staticmethod
    def is_valid_ticker(ticker: str) -> bool:
        return bool(CryptoValidator.SYMBOL_PATTERN.match(ticker))

    @staticmethod
    def is_sane_price(price: float) -> bool:
        # Ensure we are not tracking ghosts or cosmic errors
        return 0 < price < 1e12

    @classmethod
    def validate_payload(cls, data: dict) -> bool:
        required = ['symbol', 'price']
        if not all(k in data for k in required):
            return False
        return cls.is_valid_ticker(data['symbol']) and cls.is_sane_price(data['price'])

def sanitize_address(address: str) -> str:
    """Strip whitespace and force checksum casing for common chains."""
    raw = address.strip()
    return raw.lower() if raw.startswith('0x') else raw

def check_volatility(current: float, previous: float, threshold: float = 0.05) -> bool:
    """Quick math check to spot anomalies in market movement."""
    if previous == 0:
        return False
    return abs((current - previous) / previous) > threshold