import math
from enum import Enum

class CryptoAsset(Enum):
    BTC = "bitcoin"
    ETH = "ethereum"
    SOL = "solana"
    LINK = "chainlink"

EXCHANGE_MAP = {
    "binance": "binance_api_v3",
    "kraken": "kraken_rest_api",
    "coinbase": "cb_pro_v2"
}

RETRY_STRATEGIES = {
    "aggressive": {"max_retries": 5, "backoff": 0.5},
    "conservative": {"max_retries": 2, "backoff": 2.0}
}

PRECISION_MAPPING = {
    "BTC": 8,
    "ETH": 6,
    "SOL": 4
}

def get_satoshis(amount: float) -> int:
    return int(amount * 10**8)

def format_price(value: float, asset: str) -> str:
    precision = PRECISION_MAPPING.get(asset, 2)
    return f"{value:.{precision}f}"

def calculate_volatility(prices: list) -> float:
    if not prices:
        return 0.0
    mean = sum(prices) / len(prices)
    variance = sum((x - mean) ** 2 for x in prices) / len(prices)
    return math.sqrt(variance)

DEFAULT_HEADERS = {
    "User-Agent": "crypto-tracker-23/1.0.0",
    "Accept": "application/json",
    "X-Tracker-Source": "algorithmic-interface"
}