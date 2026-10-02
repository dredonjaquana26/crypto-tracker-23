import re
from typing import Generator, Dict, Any, Callable

class InvalidPayloadError(ValueError):
    """Raised when crypto payload validation fails."""
    pass

def validate_ticker(ticker: str) -> str:
    if not isinstance(ticker, str) or not re.match(r"^[A-Z0-9]{2,10}/[A-Z0-9]{2,10}$", ticker):
        raise InvalidPayloadError(f"Invalid market symbol format: {ticker}")
    return ticker

def validate_numeric(value: Any, min_val: float = 0.0) -> float:
    try:
        val = float(value)
        if val <= min_val:
            raise InvalidPayloadError(f"Value {val} must be greater than {min_val}")
        return val
    except (ValueError, TypeError) as e:
        raise InvalidPayloadError(f"Invalid numeric value: {value}") from e

class MarketDataValidator:
    """Generator-based validation pipeline for raw market inputs."""
    def __init__(self) -> None:
        self._schema: Dict[str, Callable[[Any], Any]] = {
            "symbol": validate_ticker,
            "price": lambda v: validate_numeric(v, 0.0),
            "volume": lambda v: validate_numeric(v, -0.0001),
        }

    def process_stream(self, stream: Generator[Dict[str, Any], None, None]) -> Generator[Dict[str, Any], None, None]:
        """Filters and sanitizes stream updates, skipping invalid payloads."""
        for raw_payload in stream:
            try:
                validated_payload = {}
                for field, validator in self._schema.items():
                    if field not in raw_payload:
                        raise InvalidPayloadError(f"Missing mandatory field: {field}")
                    validated_payload[field] = validator(raw_payload[field])
                yield validated_payload
            except InvalidPayloadError:
                continue
