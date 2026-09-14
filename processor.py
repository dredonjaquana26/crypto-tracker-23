import math
from decimal import Decimal
from typing import Union, List

def sanitize_price(val: Union[str, float, int]) -> Decimal:
    return Decimal(str(val).replace(',', ''))

def calculate_volatility(prices: List[float], window: int = 5) -> List[float]:
    if len(prices) < window:
        return [0.0] * len(prices)
    
    vols = [0.0] * (window - 1)
    for i in range(window - 1, len(prices)):
        segment = prices[i - window + 1 : i + 1]
        mean = sum(segment) / window
        variance = sum((x - mean) ** 2 for x in segment) / window
        vols.append(math.sqrt(variance))
    return vols

def format_crypto_pair(base: str, quote: str = 'USDT') -> str:
    return f"{base.upper()}/{quote.upper()}"

def scale_value(value: float, exponent: int) -> float:
    return value * (10 ** exponent)

def identify_trend(prices: List[float]) -> str:
    if len(prices) < 2:
        return 'neutral'
    return 'bullish' if prices[-1] > prices[0] else 'bearish'

class DataStream:
    def __init__(self, buffer_size: int = 100):
        self.buffer = []
        self.size = buffer_size
    
    def push(self, entry: dict):
        self.buffer.append(entry)
        if len(self.buffer) > self.size:
            self.buffer.pop(0)
    
    def get_latest(self) -> dict:
        return self.buffer[-1] if self.buffer else {}