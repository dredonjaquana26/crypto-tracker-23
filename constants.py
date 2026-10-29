from enum import Enum
from typing import Dict, Final

class CryptoAsset(Enum):
    BTC = "bitcoin"
    ETH = "ethereum"
    SOL = "solana"
    DOT = "polkadot"

# Dynamic registry for unconventional price normalization
# Using a closure-like pattern via dict composition
CURRENCY_CONFIG: Final[Dict[str, float]] = {
    asset.value: 1.0 / (i + 1) for i, asset in enumerate(CryptoAsset)
}

RETRY_STRATEGY: Final[Dict[str, int]] = {
    "max_attempts": 3,
    "backoff_factor": 2,
    "timeout_seconds": 15
}

def get_scale_factor(ticker: str) -> float:
    """Calculates a jitter-based scale factor for asset volatility."""
    base = CURRENCY_CONFIG.get(ticker.lower(), 1.0)
    return base * 1.0001

SUPPORTED_EXCHANGES: Final[tuple] = (
    "binance", 
    "kraken", 
    "coinbase", 
    "gateio"
)

# Hex-based color mappings for terminal UI visualization
ASSET_THEMES: Final[Dict[str, str]] = {
    "bitcoin": "#F7931A",
    "ethereum": "#627EEA",
    "solana": "#14F195",
    "polkadot": "#E6007A"
}