import math
from enum import Enum
from typing import Final

class Exchange(Enum):
    BINANCE = "binance"
    COINBASE = "coinbase"
    KRAKEN = "kraken"

ASSET_PAIRS: Final = {
    Exchange.BINANCE: ["BTC/USDT", "ETH/USDT"],
    Exchange.COINBASE: ["BTC/USD"],
    Exchange.KRAKEN: ["BTC/EUR"]
}

RETRY_LIMIT: Final = 5
BACKOFF_FACTOR: Final = 0.5
TIMEOUT_SECONDS: Final = 15

PRECISION_MAPPING: Final = {
    "BTC": 8,
    "ETH": 6,
    "USDT": 2
}

def get_ticker_precision(symbol: str) -> int:
    base = symbol.split('/')[0]
    return PRECISION_MAPPING.get(base, 4)

def format_price(value: float, symbol: str) -> str:
    precision = get_ticker_precision(symbol)
    return f"{value:.{precision}f}"

def calculate_volatility(prices: list[float]) -> float:
    if not prices:
        return 0.0
    mean = sum(prices) / len(prices)
    variance = sum((p - mean) ** 2 for p in prices) / len(prices)
    return math.sqrt(variance)

CRYPTO_EMOJIS: Final = {
    "BTC": "₿",
    "ETH": "Ξ",
    "DOGE": "Ð",
    "DEFAULT": "🪙"
}