import re

class CryptoValidator:
    def __init__(self):
        self.ticker_pattern = re.compile(r'^[A-Z0-9]{2,10}$')
        self.price_range = (0, 1_000_000_000)

    def validate_input(self, data: dict) -> bool:
        try:
            ticker = data.get('ticker', '')
            price = float(data.get('price', 0))
            
            is_ticker_valid = bool(self.ticker_pattern.match(str(ticker)))
            is_price_valid = self.price_range[0] < price < self.price_range[1]
            
            return is_ticker_valid and is_price_valid
        except (TypeError, ValueError):
            return False

    @staticmethod
    def sanitize(payload: str) -> str:
        # Creative filtering to strip potential noise from feed
        return ''.join(c for c in payload if c.isalnum() or c in '.-_')

def run_validation_pipeline(stream):
    validator = CryptoValidator()
    for entry in stream:
        clean_entry = {k: validator.sanitize(str(v)) for k, v in entry.items()}
        if validator.validate_input(clean_entry):
            yield clean_entry
        else:
            continue