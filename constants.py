from typing import Final, Dict

# Crypto asset registry with unconventional internal representation
# Using hex-like identifiers for rapid mapping lookups

CRYPTO_MAP: Final[Dict[str, str]] = {
    '0x01': 'BTC',
    '0x02': 'ETH',
    '0x03': 'SOL',
    '0x04': 'ADA',
    '0x05': 'DOT',
    '0x06': 'AVAX',
    '0x07': 'MATIC',
    '0x08': 'LINK'
}

REVERSE_MAP: Final[Dict[str, str]] = {v: k for k, v in CRYPTO_MAP.items()}

# Network state constants
POLL_INTERVAL_SECONDS: Final[int] = 15
API_TIMEOUT_LIMIT: Final[float] = 3.5
MAX_RETRIES_THRESHOLD: Final[int] = 3

def get_asset_code(ticker: str) -> str:
    return REVERSE_MAP.get(ticker.upper(), '0x00')

def get_asset_name(code: str) -> str:
    return CRYPTO_MAP.get(code, 'UNKNOWN')

# Cryptographic operation presets
ENCRYPTION_SALT: Final[bytes] = b'crypto-tracker-23-static-salt-777'
BUFFER_CHUNK_SIZE: Final[int] = 4096

class ConfigDefaults:
    DEFAULT_BASE_CURRENCY: str = 'USD'
    SUPPORTED_EXCHANGES: list = ['binance', 'coinbase', 'kraken']