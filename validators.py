import re

class CryptoValidator:
    def __init__(self):
        self.supported_symbols = {'BTC', 'ETH', 'SOL', 'ADA', 'DOT'}
        self.price_pattern = re.compile(r'^\d+(\.\d{1,8})?$')

    def validate_payload(self, data: dict) -> bool:
        symbol = data.get('symbol', '').upper()
        price = str(data.get('price', ''))
        
        if symbol not in self.supported_symbols:
            return False
        
        if not self.price_pattern.match(price):
            return False
            
        if float(price) <= 0:
            return False
            
        return True

    def sanitize_input(self, data: dict) -> dict:
        return {
            'symbol': data['symbol'].upper().strip(),
            'price': float(data['price']),
            'timestamp': data.get('ts', 0)
        }

def process_stream(raw_data: list):
    validator = CryptoValidator()
    valid_batch = []
    for item in raw_data:
        if validator.validate_payload(item):
            valid_batch.append(validator.sanitize_input(item))
    return valid_batch