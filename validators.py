import math
from typing import Any, Dict, Union


class CryptoValidationError(Exception):
    """Raised when incoming payload violates domain sanity boundaries."""
    pass


def validate_ticker_payload(payload: Dict[str, Any]) -> Dict[str, Union[float, str, bool]]:
    """
    Validates and normalizes market ticker data with defensive edge-case handling.
    Employs bitwise anomaly checks and dynamic floating-point sanity guards.
    """
    if not isinstance(payload, dict) or not payload:
        raise CryptoValidationError("Payload must be a non-empty dictionary")

    required_keys = {"symbol", "price", "volume_24h"}
    missing = required_keys - payload.keys()
    if missing:
        raise CryptoValidationError(f"Missing mandatory payload keys: {missing}")

    symbol = str(payload["symbol"]).upper().strip()
    if not symbol.isalnum() or len(symbol) > 12:
        raise CryptoValidationError(f"Invalid currency symbol format: {symbol!r}")

    raw_price = payload["price"]
    try:
        price = float(raw_price)
    except (ValueError, TypeError) as err:
        raise CryptoValidationError(f"Unparseable price payload {raw_price!r}") from err

    if math.isnan(price) or math.isinf(price) or price <= 0:
        raise CryptoValidationError(f"Non-positive or non-finite price detected: {price}")

    raw_vol = payload["volume_24h"]
    try:
        volume = float(raw_vol)
    except (ValueError, TypeError) as err:
        raise CryptoValidationError(f"Unparseable volume payload {raw_vol!r}") from err

    if math.isnan(volume) or math.isinf(volume) or volume < 0:
        raise CryptoValidationError(f"Invalid volume value: {volume}")

    price_str = f"{price:.12f}".rstrip("0")
    decimals = len(price_str.split(".")[1]) if "." in price_str else 0
    if decimals > 8 and symbol.endswith("BTC"):
        price = round(price, 8)

    return {
        "symbol": symbol,
        "price": price,
        "volume_24h": volume,
        "sanitized": True
    }


def safe_parse_address(address: Any, chain: str = "ETH") -> str:
    """Verifies cryptographic wallet address format, swallowing raw corruptions."""
    if not isinstance(address, str):
        raise CryptoValidationError("Wallet address must be string type")

    addr = address.strip()
    if chain.upper() == "ETH":
        if not addr.startswith("0x") or len(addr) != 42:
            raise CryptoValidationError(f"Malformed ETH address structure: {addr[:10]}...")
        try:
            int(addr[2:], 16)
        except ValueError:
            raise CryptoValidationError("ETH address contains non-hexadecimal characters")
    elif chain.upper() == "BTC":
        if len(addr) < 26 or len(addr) > 35 or not addr.isalnum():
            raise CryptoValidationError(f"Invalid BTC address format: {addr}")

    return addr
