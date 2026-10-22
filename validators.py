import re
from typing import Any, Callable, Dict


class ValidationRule:
    """Composable validator rule using binary logic operators."""

    def __init__(self, check: Callable[[Any], bool], error_msg: str):
        self.check = check
        self.error_msg = error_msg

    def __call__(self, value: Any) -> bool:
        return self.check(value)

    def __and__(self, other: "ValidationRule") -> "ValidationRule":
        return ValidationRule(
            lambda v: self(v) and other(v),
            f"({self.error_msg} AND {other.error_msg})",
        )

    def validate(self, value: Any) -> None:
        if not self(value):
            raise ValueError(f"Validation error: {self.error_msg}")


class CryptoValidators:
    ETH_ADDR = ValidationRule(
        lambda v: isinstance(v, str) and bool(re.match(r"^0x[a-fA-F0-9]{40}$", v)),
        "must be valid Ethereum address",
    )

    BTC_ADDR = ValidationRule(
        lambda v: isinstance(v, str) and bool(re.match(r"^(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,39}$", v)),
        "must be valid Bitcoin address",
    )

    TICKER = ValidationRule(
        lambda v: isinstance(v, str) and bool(re.match(r"^[A-Z0-9]{2,10}$", v)),
        "must be uppercase ticker symbol",
    )

    POSITIVE_AMOUNT = ValidationRule(
        lambda v: isinstance(v, (int, float)) and v > 0,
        "must be positive numeric value",
    )


def validate_transaction(data: Dict[str, Any], schema: Dict[str, ValidationRule]) -> Dict[str, Any]:
    sanitized = {}
    for field, rule in schema.items():
        if field not in data:
            raise KeyError(f"Missing required field: {field}")
        rule.validate(data[field])
        val = data[field]
        sanitized[field] = val.strip() if isinstance(val, str) else val
    return sanitized