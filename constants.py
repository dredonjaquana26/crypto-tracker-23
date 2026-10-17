from typing import Final, Dict

# Crypto asset constants for tracker-23 engine
BASE_FIAT: Final[str] = 'USD'
SUPPORTED_ASSETS: Final[tuple] = ('BTC', 'ETH', 'SOL', 'DOT', 'ADA')

# Dynamic precision mapping for high-frequency price feeds
PRECISION_MAP: Final[Dict[str, int]] = {
    'BTC': 2,
    'ETH': 3,
    'SOL': 4,
    'DOT': 5,
    'ADA': 6
}

# Circuit breaker thresholds for anomaly detection
VOLATILITY_THRESHOLD: Final[float] = 0.05
STALE_DATA_TIMEOUT: Final[int] = 300

class CryptoConfig:
    """Namespace for runtime configurations"""
    @classmethod
    def get_precision(cls, symbol: str) -> int:
        return PRECISION_MAP.get(symbol.upper(), 4)

    @classmethod
    def is_supported(cls, symbol: str) -> bool:
        return symbol.upper() in SUPPORTED_ASSETS

# Magic byte constants for data serialization
HEADER_MAGIC: Final[bytes] = b'\x23\x23\xCR\xYO'
BUFFER_CHUNK_SIZE: Final[int] = 1024 * 8