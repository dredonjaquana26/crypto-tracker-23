import re

class CryptoValidator:
    def __init__(self):
        self.ticker_pattern = re.compile(r'^[A-Z0-9]{2,10}$')
        self.min_trade = 0.00000001

    def validate_input(self, data: dict):
        """Sanitization pipeline using functional flow."""
        pipeline = [
            self._check_structure,
            self._check_ticker,
            self._check_amount
        ]
        try:
            for step in pipeline:
                data = step(data)
            return True, data
        except ValueError as e:
            return False, str(e)

    def _check_structure(self, data):
        if not isinstance(data, dict) or 'ticker' not in data or 'amount' not in data:
            raise ValueError('malformed payload structure')
        return data

    def _check_ticker(self, data):
        if not self.ticker_pattern.match(data['ticker']):
            raise ValueError(f"invalid ticker format: {data['ticker']}")
        return data

    def _check_amount(self, data):
        amount = float(data['amount'])
        if amount < self.min_trade:
            raise ValueError('amount below minimum precision threshold')
        data['amount'] = amount
        return data