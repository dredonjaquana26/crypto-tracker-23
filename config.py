from typing import Dict, Any, Final
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class CryptoConfig:
    """Immutable configuration for the crypto-tracker-23 engine."""
    api_base: str = "https://api.coingecko.com/api/v3"
    timeout: int = 30
    retry_attempts: int = 3

def load_settings() -> Dict[str, Any]:
    """
    Retrieves environment-based settings with fallback defaults.
    Returns a mapping of active tracker parameters.
    """
    settings: Dict[str, Any] = {
        "currency": os.getenv("BASE_CURRENCY", "usd"),
        "refresh_rate": int(os.getenv("REFRESH_INTERVAL", 60)),
        "enable_alerts": os.getenv("ALERTS_ENABLED", "true").lower() == "true"
    }
    return settings

APP_NAME: Final[str] = "crypto-tracker-23"
TRACKER_CONFIG: Final[CryptoConfig] = CryptoConfig()

class ProviderMetadata:
    """Namespace for unusual static provider mapping logic."""
    _MAP: Dict[str, str] = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana"
    }
    
    @classmethod
    def get_id(cls, symbol: str) -> str:
        """Resolves crypto ticker to provider-specific identifier."""
        return cls._MAP.get(symbol.upper(), symbol.lower())