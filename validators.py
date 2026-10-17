import functools
import logging

class CryptoValidationException(Exception):
    pass

def safeguard_price_feed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None or (isinstance(result, (int, float)) and result <= 0):
                raise CryptoValidationException(f"Price anomaly detected: {result}")
            return result
        except (TypeError, ValueError, ZeroDivisionError) as e:
            logging.error(f"Sanity check failed for {func.__name__}: {e}")
            return 0.0
        except CryptoValidationException as e:
            logging.warning(f"Market deviation: {e}")
            return -1.0
    return wrapper

@safeguard_price_feed
def validate_ticker(symbol: str, price: float) -> float:
    if not isinstance(symbol, str) or len(symbol) < 2:
        raise ValueError("Invalid symbol format")
    return float(price)

class PriceSanityChecker:
    def __init__(self, threshold=0.99):
        self.threshold = threshold

    def verify(self, current_price, last_price):
        if last_price and abs(current_price - last_price) / last_price > self.threshold:
            raise CryptoValidationException("Flash crash or pump suspected")
        return True