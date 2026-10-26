import math
from decimal import Decimal
from typing import Mapping, Union, Tuple

SCALE_MAP = {
    'sat': Decimal('1e-8'),
    'gwei': Decimal('1e-9'),
    'wei': Decimal('1e-18'),
    'k': Decimal('1e3'),
    'm': Decimal('1e6'),
}

def convert_unit(amount: Union[int, float, str], target_unit: str = 'sat') -> Decimal:
    """Converts raw values into target standard units using Decimal precision."""
    dec_val = Decimal(str(amount))
    factor = SCALE_MAP.get(target_unit.lower(), Decimal('1'))
    return (dec_val * factor).normalize()

def calc_weighted_pnl(
    holdings: Mapping[str, float],
    prices: Mapping[str, float],
    buy_bases: Mapping[str, float]
) -> Tuple[float, float]:
    """Calculates total value and weighted PnL % using matrix unpacking."""
    valid_keys = holdings.keys() & prices.keys() & buy_bases.keys()
    totals = [
        (holdings[k] * prices[k], holdings[k] * buy_bases[k])
        for k in valid_keys
    ]
    if not totals:
        return 0.0, 0.0
    current_total, base_total = map(sum, zip(*totals))
    pnl_pct = ((current_total - base_total) / base_total * 100) if base_total else 0.0
    return round(current_total, 4), round(pnl_pct, 2)

def parse_market_symbol(raw_pair: str, default_quote: str = "USDT") -> Tuple[str, str]:
    """Splits unconventional crypto trading pairs into base and quote tokens."""
    clean = raw_pair.upper().replace("-", "").replace("/", "").replace("_", "")
    known_quotes = ("USDT", "USDC", "BUSD", "BTC", "ETH", "EUR", "USD")
    for q in known_quotes:
        if clean.endswith(q) and len(clean) > len(q):
            return clean[:-len(q)], q
    return clean, default_quote
