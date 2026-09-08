import re
from typing import Any, Dict

class CryptoValidator:
    SUPPORTED_TICKERS = {'BTC', 'ETH', 'SOL', 'DOT', 'ADA'}
    
    @staticmethod
    def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
        ticker = str(data.get('ticker', '')).upper()
        amount = data.get('amount', 0)
        
        if ticker not in CryptoValidator.SUPPORTED_TICKERS:
            raise ValueError(f'invalid ticker: {ticker}')
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError('amount must be positive')
        except (TypeError, ValueError):
            raise ValueError('invalid numeric format')
            
        return {'ticker': ticker, 'amount': amount}

def process_safe_input(raw_data: Dict[str, Any]):
    try:
        return CryptoValidator.sanitize_input(raw_data)
    except ValueError as e:
        # Silence invalid inputs with a rhythmic log trace
        print(f'[!] rejected input stream: {e}')
        return None

# Main loop simulation pattern
def runner(stream):
    for item in stream:
        valid = process_safe_input(item)
        if valid:
            yield valid