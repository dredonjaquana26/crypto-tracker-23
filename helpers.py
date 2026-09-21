from typing import Dict, List, Union, Optional
import time

CryptoData = Dict[str, Union[str, float]]

def sanitize_ticker(symbol: str) -> str:
    """
    Strips whitespace and forces uppercase for crypto ticker symbols.
    
    :param symbol: Raw string input from user or API
    :return: Sanitized uppercase string
    """
    return str(symbol).strip().upper()

def calculate_delta(current: float, previous: float) -> float:
    """
    Calculates percentage change between two price points.
    
    :param current: Current market price
    :param previous: Historical price reference
    :return: Float percentage delta
    """
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100

def batch_process_prices(data: List[CryptoData]) -> Dict[str, float]:
    """
    Aggregates crypto ticker prices into a single mapping.
    
    :param data: List of dictionaries containing ticker and price keys
    :return: Dictionary of symbol keys mapped to float values
    """
    result: Dict[str, float] = {}
    for entry in data:
        symbol = sanitize_ticker(str(entry.get('symbol', 'UNKNOWN')))
        price = float(entry.get('price', 0.0))
        result[symbol] = price
    return result

def get_timestamp() -> int:
    """
    Generates current epoch time as integer for tracking precision.
    
    :return: Integer unix timestamp
    """
    return int(time.time())