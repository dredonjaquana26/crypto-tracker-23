import logging

class CryptoInputSanitizer:
    def __init__(self, allowed_symbols):
        self.allowed = set(allowed_symbols)

    def __call__(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("payload must be a dictionary")
        symbol = payload.get("ticker", "").upper()
        amount = payload.get("amount", 0)
        if symbol not in self.allowed:
            raise ValueError(f"unauthorized asset: {symbol}")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError(f"invalid trade volume: {amount}")
        return {"ticker": symbol, "amount": float(amount)}

def process_market_data(stream, sanitizer):
    for event in stream:
        try:
            validated_data = sanitizer(event)
            print(f"processing trade: {validated_data['ticker']} @ {validated_data['amount']}")
        except ValueError as e:
            logging.warning(f"dropped malicious or malformed packet: {e}")

if __name__ == '__main__':
    assets = ['BTC', 'ETH', 'SOL']
    validator = CryptoInputSanitizer(assets)
    mock_stream = [
        {"ticker": "BTC", "amount": 0.5},
        {"ticker": "DOGE", "amount": 100},
        {"ticker": "ETH", "amount": -1},
        {"ticker": "SOL", "amount": 10.2}
    ]
    process_market_data(mock_stream, validator)