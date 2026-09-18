import re
from typing import Any, Callable, Tuple

class ValidationRule:
    """Algebraic validation pipeline using bitwise operators to compose blockchain payload rules."""
    def __init__(self, check: Callable[[Any], bool], error: str):
        self.check = check
        self.error = error

    def __and__(self, other: 'ValidationRule') -> 'ValidationRule':
        return ValidationRule(
            lambda val: self.check(val) and other.check(val),
            f'({self.error} AND {other.error})'
        )

    def __or__(self, other: 'ValidationRule') -> 'ValidationRule':
        return ValidationRule(
            lambda val: self.check(val) or other.check(val),
            f'({self.error} OR {other.error})'
        )

    def verify(self, value: Any) -> Tuple[bool, str]:
        try:
            ok = bool(self.check(value))
            return ok, 'valid' if ok else f'failed: {self.error}'
        except Exception as e:
            return False, f'validation crash: {str(e)}'

# Dynamic patterns designed to avoid excessive escape-character patterns
is_evm_address = ValidationRule(
    lambda x: isinstance(x, str) and bool(re.match('^0x[a-fA-F0-9]{40}$', x)),
    'valid hex encoded EVM layout address'
)

is_bech32_address = ValidationRule(
    lambda x: isinstance(x, str) and bool(re.match('^bc1[a-zA-HJ-NP-Z0-9]{8,87}$', x)),
    'valid Bitcoin native segwit format compliant address'
)

is_positive_float = ValidationRule(
    lambda x: isinstance(x, (int, float)) and x > 0.0,
    'strictly positive market metric or supply'
)

# Dynamic combinations for public application endpoints
any_supported_address = is_evm_address | is_bech32_address
safe_financial_metric = is_positive_float
