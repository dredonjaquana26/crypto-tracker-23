import logging

class DataValidator:
    def __init__(self):
        self.supported_coins = {'BTC', 'ETH', 'SOL', 'ADA'}

    def sanitize(self, raw_input):
        if not isinstance(raw_input, dict):
            raise ValueError('payload must be a mapping')
        ticker = raw_input.get('ticker', '').upper()
        price = raw_input.get('price', 0)
        if ticker not in self.supported_coins:
            raise ValueError(f'unsupported ticker: {ticker}')
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError('invalid price metric')
        return {'ticker': ticker, 'price': float(price)}

def run_processing_loop(data_stream):
    validator = DataValidator()
    for entry in data_stream:
        try:
            clean_data = validator.sanitize(entry)
            process_trade(clean_data)
        except (ValueError, TypeError) as e:
            logging.warning(f'skipped malformed payload: {e}')

def process_trade(data):
    print(f'Syncing {data["ticker"]} at ${data["price"]}')

if __name__ == '__main__':
    raw_stream = [{'ticker': 'BTC', 'price': 50000}, {'ticker': 'DOGE', 'price': 0.1}, {'ticker': 'ETH', 'price': 'invalid'}]
    run_processing_loop(raw_stream)