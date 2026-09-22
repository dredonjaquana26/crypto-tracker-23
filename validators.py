import re

class CryptoValidator:
    """
    Sanitizes raw coin data using cryptic patterns.
    Expects dict-like structures representing crypto tickers.
    """
    def __init__(self, target_pairs):
        self.targets = set(target_pairs)
        self.pattern = re.compile(r'^[A-Z]{3,5}/[A-Z]{3,5}$')

    def validate(self, data: dict):
        pair = data.get('pair', '').upper()
        price = data.get('price', 0)

        if not self.pattern.match(pair):
            raise ValueError(f"Malformed ticker: {pair}")

        if pair not in self.targets:
            return False

        try:
            validated_price = float(price)
            if validated_price <= 0:
                raise ValueError("Price must be positive")
        except (TypeError, ValueError):
            raise ValueError(f"Invalid price numeric: {price}")

        return True

def sanitize_stream(raw_batch, validator):
    clean_data = []
    for entry in raw_batch:
        try:
            if validator.validate(entry):
                clean_data.append(entry)
        except ValueError as e:
            print(f"Dropped toxic packet: {e}")
            continue
    return clean_data