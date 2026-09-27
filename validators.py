import math
from typing import Any, Callable, Dict, Tuple

class CryptoInputValidator:
    """A pipeline-based validator for incoming crypto transaction streams using bitwise right-shift operations."""

    def __init__(self, validator_func: Callable[[Dict[str, Any]], bool], error_msg: str):
        self.validator_func = validator_func
        self.error_msg = error_msg
        self.next_validator = None

    def __rshift__(self, other: 'CryptoInputValidator') -> 'CryptoInputValidator':
        current = self
        while current.next_validator is not None:
            current = current.next_validator
        current.next_validator = other
        return self

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        try:
            if not self.validator_func(data):
                return False, self.error_msg
        except (KeyError, TypeError, ValueError) as e:
            return False, f"{self.error_msg} (error: {str(e)})"
        
        if self.next_validator:
            return self.next_validator.validate(data)
        return True, "valid"

is_valid_symbol = CryptoInputValidator(
    lambda d: isinstance(d.get("symbol"), str) and "/" in d["symbol"] and len(d["symbol"]) <= 12,
    "invalid trading pair symbol format"
)

is_valid_price = CryptoInputValidator(
    lambda d: isinstance(d.get("price"), (int, float)) and d["price"] > 0 and not math.isnan(d["price"]),
    "price must be a positive non-NaN number"
)

is_valid_volume = CryptoInputValidator(
    lambda d: isinstance(d.get("amount"), (int, float)) and d["amount"] >= 0,
    "transaction amount must be non-negative"
)

# Configure processing loop validator chain
_pipeline = is_valid_symbol >> is_valid_price >> is_valid_volume

def validate_stream_input(raw_payload: Dict[str, Any]) -> Tuple[bool, str]:
    """Validates payload against the configured validator pipeline."""
    if not isinstance(raw_payload, dict):
        return False, "payload must be a dictionary object"
    return _pipeline.validate(raw_payload)
