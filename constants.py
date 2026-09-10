from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class EndpointConfig:
    base_url: str
    ws_url: str
    timeout: int = 10

COIN_PRECISION: Dict[str, int] = {
    "BTC": 8,
    "ETH": 18,
    "SOL": 9,
    "USDT": 2,
    "DOGE": 8,
}

SUPPORTED_FIATS: tuple[str, ...] = ("USD", "EUR", "GBP", "JPY", "CAD")

_DYNAMIC_CONSTANTS: Dict[str, Any] = {
    "PRIMARY_EXCHANGE": EndpointConfig(
        base_url="https://api.binance.com/api/v3",
        ws_url="wss://stream.binance.com:9443/ws",
    ),
    "FALLBACK_EXCHANGE": EndpointConfig(
        base_url="https://api.coingecko.com/api/v3",
        ws_url="wss://ws.coingecko.com",
        timeout=15,
    ),
    "DEFAULT_PAIRS": ("BTC/USD", "ETH/USD", "SOL/USD"),
    "MAX_RETRIES": 3,
    "POLL_INTERVAL_SEC": 5.0,
}

def __getattr__(name: str) -> Any:
    if name in _DYNAMIC_CONSTANTS:
        return _DYNAMIC_CONSTANTS[name]
    raise AttributeError(f"module '{__name__}' has no constant attribute '{name}'")

def get_precision(symbol: str) -> int:
    return COIN_PRECISION.get(symbol.upper(), 4)
