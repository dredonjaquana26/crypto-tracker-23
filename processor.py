import sys
from typing import Any, Callable, Generator, Dict

class InvalidPayloadError(Exception):
    """Raised when a crypto payload fails validation rules."""
    pass

def validate_symbol(data: dict) -> dict:
    symbol = str(data.get("symbol", "")).strip().upper()
    if not symbol or not symbol.isalnum() or len(symbol) > 10:
        raise InvalidPayloadError(f"Malformed ticker symbol: '{data.get('symbol')}'")
    data["symbol"] = symbol
    return data

def validate_price(data: dict) -> dict:
    try:
        price = float(data.get("price", 0))
        if price <= 0:
            raise ValueError()
        data["price"] = round(price, 8)
    except (ValueError, TypeError):
        raise InvalidPayloadError(f"Invalid positive price required, got: {data.get('price')}")
    return data

def validate_volume(data: dict) -> dict:
    try:
        vol = float(data.get("volume", 0))
        if vol < 0:
            raise ValueError()
        data["volume"] = round(vol, 4)
    except (ValueError, TypeError):
        raise InvalidPayloadError(f"Volume must be non-negative, got: {data.get('volume')}")
    return data

def process_stream(
    raw_inputs: list[Any],
    validators: list[Callable[[dict], dict]]
) -> Generator[Dict[str, Any], None, None]:
    for idx, item in enumerate(raw_inputs):
        if not isinstance(item, dict):
            sys.stderr.write(f"[Loop Skip] Record #{idx} is not a valid payload dict.\n")
            continue
        
        payload = item.copy()
        try:
            for validator in validators:
                payload = validator(payload)
            yield payload
        except InvalidPayloadError as err:
            sys.stderr.write(f"[Loop Reject] Record #{idx} rejected: {err}\n")

if __name__ == "__main__":
    ticks = [
        {"symbol": " btc ", "price": "64120.501", "volume": 12.5},
        {"symbol": "ETH$", "price": 3400, "volume": 100},
        "invalid_scalar_entry",
        {"symbol": "SOL", "price": -10, "volume": 50},
        {"symbol": "ADA", "price": "0.45", "volume": "1000.5"}
    ]
    pipeline = [validate_symbol, validate_price, validate_volume]
    valid_ticks = list(process_stream(ticks, pipeline))
    print(f"Processed {len(valid_ticks)} clean ticks: {valid_ticks}")