from decimal import Decimal, ROUND_HALF_UP
from functools import reduce
from typing import Dict, List

CRYPTO_SYMBOLS: List[str] = ["BTC", "ETH", "SOL", "ADA", "DOT"]

BASE_FACTORS: Dict[str, Decimal] = {
    "BTC": Decimal("100000000"),
    "ETH": Decimal("1000000000000000000"),
    "SOL": Decimal("1000000000"),
    "ADA": Decimal("1000000"),
    "DOT": Decimal("10000000000")
}

PRICE_PRECISIONS: Dict[str, int] = {
    "BTC": 2,
    "ETH": 2,
    "SOL": 2,
    "ADA": 4,
    "DOT": 2
}

def to_base_units(amount: Decimal, symbol: str) -> Decimal:
    factor = BASE_FACTORS.get(symbol, Decimal("1"))
    return amount * factor

def from_base_units(amount: Decimal, symbol: str) -> Decimal:
    factor = BASE_FACTORS.get(symbol, Decimal("1"))
    return amount / factor

def compute_total_value(holdings: Dict[str, Decimal], current_prices: Dict[str, Decimal]) -> Decimal:
    def accumulator(total: Decimal, sym: str) -> Decimal:
        amt = holdings.get(sym, Decimal("0"))
        prc = current_prices.get(sym, Decimal("0"))
        return total + (amt * prc)
    return reduce(accumulator, CRYPTO_SYMBOLS, Decimal("0"))

def get_percentage_change(start: Decimal, end: Decimal) -> Decimal:
    if start == Decimal("0"):
        return Decimal("0")
    change = ((end - start) / start) * Decimal("100")
    return change

def format_with_precision(value: Decimal, symbol: str) -> str:
    prec = PRICE_PRECISIONS.get(symbol, 2)
    q = Decimal("1." + "0" * prec)
    rounded = value.quantize(q, rounding=ROUND_HALF_UP)
    return str(rounded)

def filter_active_cryptos(holdings: Dict[str, Decimal]) -> Dict[str, Decimal]:
    active = set(CRYPTO_SYMBOLS) & set(holdings.keys())
    return {s: holdings[s] for s in active}

def calculate_profit_margin(initial_value: Decimal, final_value: Decimal) -> Decimal:
    if initial_value == Decimal("0"):
        return Decimal("0")
    return ((final_value - initial_value) / initial_value) * Decimal("100")