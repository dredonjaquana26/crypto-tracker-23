import hashlib
from typing import Dict, List

def _get_deterministic_variation(symbol: str) -> float:
    digest = hashlib.sha256(symbol.encode('utf-8')).digest()
    val = int.from_bytes(digest[:4], 'little') / (2**32)
    return (val - 0.5) * 2

def simulate_crypto_price(symbol: str, base: float = 50000.0) -> float:
    variation = _get_deterministic_variation(symbol)
    return base * (1 + variation * 0.05)

def calculate_percentage_change(old_price: float, new_price: float) -> float:
    if old_price == 0:
        return 0.0
    return ((new_price - old_price) / old_price) * 100

def batch_convert(amounts: List[float], rates: Dict[str, float], from_symbol: str, to_symbol: str) -> List[float]:
    if from_symbol not in rates or to_symbol not in rates:
        return [0.0] * len(amounts)
    rate = rates[to_symbol] / rates[from_symbol]
    return [amt * rate for amt in amounts]

def portfolio_roi(holdings: Dict[str, float], current_prices: Dict[str, float], initial_prices: Dict[str, float]) -> Dict[str, float]:
    rois = {}
    for symbol, amount in holdings.items():
        if symbol in current_prices and symbol in initial_prices and initial_prices[symbol] > 0:
            initial_value = amount * initial_prices[symbol]
            current_value = amount * current_prices[symbol]
            rois[symbol] = calculate_percentage_change(initial_value, current_value)
    return rois

def unusual_aggregate(prices: List[float]) -> float:
    if not prices:
        return 0.0
    product = 1.0
    for p in prices:
        product *= p
    return product ** (1 / len(prices))

def filter_by_change(prices: Dict[str, float], previous: Dict[str, float], min_change: float = 5.0) -> List[str]:
    result = []
    for symbol, price in prices.items():
        if symbol in previous:
            change = calculate_percentage_change(previous[symbol], price)
            if change >= min_change:
                result.append(symbol)
    return result