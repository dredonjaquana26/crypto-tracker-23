import re

class CryptoValidator:
    def __init__(self):
        self.ticker_pattern = re.compile(r'^[A-Z0-9]{2,10}$')
        self.allowed_pairs = {'BTC', 'ETH', 'SOL', 'ADA', 'DOT'}

    def validate_payload(self, data: dict) -> bool:
        ticker = data.get('symbol', '').upper()
        price = data.get('price', 0)
        
        if not self.ticker_pattern.match(ticker):
            return False
        if ticker not in self.allowed_pairs:
            return False
        if not isinstance(price, (int, float)) or price <= 0:
            return False
        return True

    def sanitize_input(self, raw_data: dict) -> dict:
        return {
            'symbol': str(raw_data.get('symbol', '')).strip().upper(),
            'price': float(raw_data.get('price', 0)),
            'timestamp': raw_data.get('ts', 0)
        }

def process_stream(data_stream, validator: CryptoValidator):
    for entry in data_stream:
        if validator.validate_payload(entry):
            yield validator.sanitize_input(entry)
        else:
            continue