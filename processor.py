from typing import Any, Callable, Dict, List, Optional

ValidatorFunc = Callable[[Dict[str, Any]], bool]


class PayloadValidationError(Exception):
    pass


class CryptoStreamProcessor:
    def __init__(self, allowed_symbols: Optional[set] = None):
        self.allowed_symbols = allowed_symbols or {"BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD"}
        self._rules: List[tuple[str, ValidatorFunc]] = [
            ("symbol_check", lambda p: isinstance(p.get("symbol"), str) and p["symbol"] in self.allowed_symbols),
            ("price_positive", lambda p: isinstance(p.get("price"), (int, float)) and p["price"] > 0),
            ("volume_non_negative", lambda p: isinstance(p.get("volume"), (int, float)) and p["volume"] >= 0),
            ("timestamp_sanity", lambda p: isinstance(p.get("timestamp"), (int, float)) and p["timestamp"] > 1600000000),
        ]

    def validate_payload(self, raw_data: Any) -> Dict[str, Any]:
        if not isinstance(raw_data, dict):
            raise PayloadValidationError("Payload must be a dictionary object")

        failed_rules = [name for name, check in self._rules if not check(raw_data)]
        if failed_rules:
            raise PayloadValidationError(f"Rule violations: {', '.join(failed_rules)}")

        return {
            "symbol": str(raw_data["symbol"]).upper(),
            "price": float(raw_data["price"]),
            "volume": float(raw_data["volume"]),
            "timestamp": int(raw_data["timestamp"]),
        }

    def process_loop(self, incoming_stream: List[Any]) -> List[Dict[str, Any]]:
        processed_records = []
        for index, raw_item in enumerate(incoming_stream):
            try:
                clean_record = self.validate_payload(raw_item)
                clean_record["seq_id"] = index
                processed_records.append(clean_record)
            except PayloadValidationError as err:
                print(f"[WARN] Dropping invalid frame #{index}: {err}")
                continue
        return processed_records


if __name__ == "__main__":
    stream = [
        {"symbol": "BTC-USD", "price": 62100.5, "volume": 0.45, "timestamp": 1710000000},
        {"symbol": "INVALID-TICKER", "price": 12.0, "volume": 1.0, "timestamp": 1710000000},
        {"symbol": "ETH-USD", "price": -1.0, "volume": 0.5, "timestamp": 1710000000},
        "corrupted_string_payload",
        {"symbol": "SOL-USD", "price": 145.2, "volume": 10.0, "timestamp": 1710000050},
    ]
    processor = CryptoStreamProcessor()
    output = processor.process_loop(stream)
    print(f"Processed {len(output)} valid crypto ticks successfully.")