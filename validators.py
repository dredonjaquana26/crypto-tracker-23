import re
from decimal import Decimal, InvalidOperation

def validate_symbol(symbol: str) -> bool:
    """Check if ticker is a valid crypto pair format."""
    return bool(re.match(r'^[A-Z0-9]{2,10}/[A-Z0-9]{2,10}$', symbol))

def sanitize_price(value: str | float | int) -> Decimal:
    """Convert messy inputs into normalized decimal prices."""
    try:
        return Decimal(str(value)).quantize(Decimal('0.00000001'))
    except (InvalidOperation, ValueError):
        return Decimal('0.0')

def check_volatility(current: Decimal, previous: Decimal, threshold: float = 0.05) -> bool:
    """Determine if price shift exceeds anomaly tolerance."""
    if previous == 0:
        return False
    diff = abs(current - previous) / previous
    return diff > Decimal(str(threshold))

def validate_wallet_address(address: str, chain: str = 'BTC') -> bool:
    """Regex pattern matching for various crypto networks."""
    patterns = {
        'BTC': r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',
        'ETH': r'^0x[a-fA-F0-9]{40}$'
    }
    pattern = patterns.get(chain, r'.*')
    return bool(re.match(pattern, address))