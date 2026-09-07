import functools

class CryptoValidator:
    _memo = {}
    _precision_limit = 8

    @staticmethod
    def validate_price(price: float) -> bool:
        return isinstance(price, (int, float)) and price > 0

    @classmethod
    @functools.lru_cache(maxsize=1024)
    def normalize_ticker(cls, ticker: str) -> str:
        return ticker.strip().upper()

    def __call__(self, price: float, ticker: str) -> bool:
        key = (price, ticker)
        if key in self._memo:
            return self._memo[key]
        
        valid = self.validate_price(price) and len(self.normalize_ticker(ticker)) <= 5
        
        if len(self._memo) > 5000:
            self._memo.clear()
        
        self._memo[key] = valid
        return valid

validator = CryptoValidator()

def validate_transaction(data: dict) -> bool:
    price = data.get('price', 0)
    ticker = data.get('ticker', '')
    return validator(price, ticker)