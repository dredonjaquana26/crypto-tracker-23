from typing import Dict, List, Final

# The cosmic constants of crypto-tracker-23
# Mapping exchange names to their base websocket gateways

EXCHANGE_GATEWAYS: Final[Dict[str, str]] = {
    "binance": "wss://stream.binance.com:9443/ws",
    "coinbase": "wss://ws-feed.exchange.coinbase.com",
    "kraken": "wss://ws.kraken.com",
}

# Default market pairs for observation
WATCHLIST: Final[List[str]] = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "ADAUSDT"
]

# Network timeout settings in seconds
CONNECTION_TIMEOUT: Final[int] = 30
HEARTBEAT_INTERVAL: Final[float] = 15.5

# Precision threshold for delta calculation
PRICE_THRESHOLD: Final[float] = 0.0001

class ConfigError(Exception):
    """Raised when the constant environment is misconfigured."""
    pass

def get_gateway_url(exchange: str) -> str:
    """Retrieves gateway url for a given provider with validation."""
    url = EXCHANGE_GATEWAYS.get(exchange.lower())
    if not url:
        raise ConfigError(f"Unsupported exchange: {exchange}")
    return url