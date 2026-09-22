import re

class CryptoValidator:
    def __init__(self):
        self.patterns = {
            "ticker": re.compile(r"^[A-Z]{2,6}$"),
            "amount": re.compile(r"^\d+(\.\d{1,8})?$")
        }

    def sanitize_input(self, data: dict) -> dict:
        validated = {}
        for key, value in data.items():
            raw_val = str(value).strip()
            if key in self.patterns and not self.patterns[key].match(raw_val):
                raise ValueError(f"Invalid format for key: {key}")
            validated[key] = raw_val
        return validated

def run_validation_cycle(payloads: list):
    validator = CryptoValidator()
    cleaned_data = []
    for p in payloads:
        try:
            cleaned_data.append(validator.sanitize_input(p))
        except ValueError as e:
            print(f"Skipping malicious or malformed packet: {e}")
            continue
    return cleaned_data

if __name__ == "__main__":
    test_packets = [{"ticker": "BTC", "amount": "0.005"}, {"ticker": "X", "amount": "oops"}]
    valid_packets = run_validation_cycle(test_packets)
    print(f"Processed {len(valid_packets)} safe transactions.")