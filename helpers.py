import decimal
from typing import Union, Optional

def calculate_profit_margin(buy_price: Union[float, str], sell_price: Union[float, str]) -> float:
    """
    calculates the percentage gain or loss between two crypto price points.
    treats inputs as high-precision decimals to avoid floating point sorcery.
    """
    buy = decimal.Decimal(str(buy_price))
    sell = decimal.Decimal(str(sell_price))
    if buy == 0:
        return 0.0
    margin = ((sell - buy) / buy) * 100
    return float(margin.quantize(decimal.Decimal('0.0001')))

def format_crypto_ticker(symbol: str, exchange: Optional[str] = None) -> str:
    """
    standardizes crypto symbols into the canonical 'SYMBOL-EXCHANGE' format.
    handles aggressive upper-casing for messy upstream api data.
    """
    clean_symbol = symbol.strip().upper()
    clean_exchange = (exchange or 'GLOBAL').strip().upper()
    return f"{clean_symbol}-{clean_exchange}"

def check_threshold_alert(price: float, threshold: float, direction: str = 'above') -> bool:
    """
    logical gate for volatility triggers.
    evaluates if the market price has crossed the user defined barrier.
    """
    if direction == 'above':
        return price > threshold
    return price < threshold