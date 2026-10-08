import logging
import functools
import sys

class CryptoGuardian:
    def __init__(self, name='crypto-tracker-23'):
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

def resilient_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            logging.error(f"Network ripple detected in {func.__name__}: {e}")
        except ValueError as e:
            logging.warning(f"Data corruption anomaly in {func.__name__}: {e}")
        except Exception as e:
            logging.critical(f"Catastrophic blockchain state failure: {type(e).__name__}")
            return None
    return wrapper

def log_market_event(event_type, details):
    guard = CryptoGuardian()
    if not isinstance(details, dict):
        guard.logger.error("Invalid telemetry format received")
        return
    
    msg = f"EVENT:{event_type} | PAYLOAD:{str(details)[:50]}"
    guard.logger.info(msg)

if __name__ == '__main__':
    log_market_event('TICKER_FETCH', {'symbol': 'BTC', 'status': 'volatile'})