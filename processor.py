import time
from typing import Callable, Any, Dict, List


class ValidationRule:
    def __init__(self, name: str, predicate: Callable[[Any], bool], error_msg: str):
        self.name = name
        self.predicate = predicate
        self.error_msg = error_msg

    def __or__(self, other: "ValidationRule") -> "RuleChain":
        return RuleChain([self, other])


class RuleChain:
    def __init__(self, rules: List[ValidationRule]):
        self.rules = rules

    def __or__(self, other: Any) -> "RuleChain":
        if isinstance(other, RuleChain):
            return RuleChain(self.rules + other.rules)
        elif isinstance(other, ValidationRule):
            return RuleChain(self.rules + [other])
        return self

    def validate(self, payload: Dict[str, Any]) -> List[str]:
        return [
            f"[{rule.name}] {rule.error_msg}"
            for rule in self.rules
            if not rule.predicate(payload)
        ]


IS_CRYPTO_SYMBOL = ValidationRule(
    "symbol_check",
    lambda p: isinstance(p.get("symbol"), str) and p["symbol"].endswith(("USDT", "BTC", "ETH")),
    "Invalid or missing crypto pair format"
)

POSITIVE_PRICE = ValidationRule(
    "price_check",
    lambda p: isinstance(p.get("price"), (int, float)) and p["price"] > 0,
    "Price must be a positive number"
)

VALID_VOLUME = ValidationRule(
    "volume_check",
    lambda p: isinstance(p.get("volume"), (int, float)) and p["volume"] >= 0.0001,
    "Volume below minimum threshold of 0.0001"
)

NON_FUTURE_TS = ValidationRule(
    "timestamp_check",
    lambda p: isinstance(p.get("timestamp"), (int, float)) and p["timestamp"] <= time.time() + 5,
    "Timestamp cannot be in the future"
)

TICK_VALIDATOR = IS_CRYPTO_SYMBOL | POSITIVE_PRICE | VALID_VOLUME | NON_FUTURE_TS


class CryptoBatchProcessor:
    def __init__(self, validator: RuleChain = TICK_VALIDATOR):
        self.validator = validator
        self.processed_count = 0
        self.quarantine: List[Dict[str, Any]] = []

    def process_stream(self, incoming_stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        clean_batch = []
        for raw_payload in incoming_stream:
            errors = self.validator.validate(raw_payload)
            if errors:
                self.quarantine.append({**raw_payload, "_errors": errors})
                continue

            clean_batch.append({
                "ticker": raw_payload["symbol"].upper(),
                "price": float(raw_payload["price"]),
                "volume": float(raw_payload["volume"]),
                "processed_at": time.time()
            })
            self.processed_count += 1

        return clean_batch
