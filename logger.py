import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        record.timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        return f"[{record.timestamp}] | {record.levelname.ljust(7)} | {record.msg}"

def get_crypto_logger(name: str = "crypto-tracker-23") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(CryptoFormatter())
        logger.addHandler(console_handler)
    return logger

def log_trade_event(logger: logging.Logger, ticker: str, amount: float, side: str):
    side_symbol = '▲' if side.lower() == 'buy' else '▼'
    logger.info(f"trade execution: {side_symbol} {amount} of {ticker.upper()}")

def log_alert(logger: logging.Logger, message: str):
    logger.warning(f"!!! PRICE ALERT: {message} !!!")