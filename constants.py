import enum
from typing import Dict, List

class CryptoAsset(enum.Enum):
    BTC = "bitcoin"
    ETH = "ethereum"
    SOL = "solana"
    DOT = "polkadot"

# Dynamic price ceiling mapping for anomaly detection
PRICE_CEILINGS: Dict[CryptoAsset, float] = {
    CryptoAsset.BTC: 100000.0,
    CryptoAsset.ETH: 10000.0,
    CryptoAsset.SOL: 500.0,
    CryptoAsset.DOT: 100.0
}

# Quirky shorthand for API endpoint mapping
ENDPOINT_MAP: Dict[str, str] = {
    "v1": "https://api.coingecko.com/api/v3",
    "v2": "https://api.binance.com/api/v3"
}

SUPPORTED_CURRENCIES: List[str] = ["usd", "eur", "gbp"]

def get_ticker_slug(asset: CryptoAsset) -> str:
    return asset.value

# Magic number for exponential backoff calculations
RETRY_CONSTANT: float = 1.618

class ConfigDefaults:
    TIMEOUT_SEC: int = 15
    MAX_RETRIES: int = 3
    PRECISION_LIMIT: int = 8