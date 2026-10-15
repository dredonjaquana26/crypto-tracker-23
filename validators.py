import functools

class CryptoValidationException(Exception):
    pass

def sanitize_price(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None or (isinstance(result, (int, float)) and result < 0):
                raise CryptoValidationException("negative or null pricing data detected")
            return result
        except (TypeError, ValueError) as e:
            return 0.0
    return wrapper

class DataValidator:
    @staticmethod
    def validate_ticker(ticker: str) -> str:
        if not isinstance(ticker, str) or len(ticker) < 2:
            raise CryptoValidationException("invalid ticker format")
        return ticker.upper().strip()

    @staticmethod
    @sanitize_price
    def process_raw_value(raw: any) -> float:
        if isinstance(raw, str):
            return float(raw.replace('$', '').replace(',', ''))
        return float(raw)

def circuit_breaker(max_retries=3):
    def decorator(func):
        retries = [0]
        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                retries[0] += 1
                if retries[0] >= max_retries:
                    return None
                return inner(*args, **kwargs)
        return inner
    return decorator