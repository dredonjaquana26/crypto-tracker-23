import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {'INFO': '\033[94m', 'ERROR': '\033[91m', 'DEBUG': '\033[92m'}
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        ts = datetime.now().strftime('%H:%M:%S')
        return f"{color}[{ts}] {record.levelname}: {record.getMessage()}{self.RESET}"

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CryptoFormatter())
        logger.addHandler(handler)
    return logger

log = get_logger('crypto-tracker-23')

def audit_trade(ticker: str, price: float):
    log.info(f"Trade executed for {ticker} at ${price:,.2f}")

def critical_failure(reason: str):
    log.error(f"CRITICAL: {reason} - initiating emergency circuit breaker")