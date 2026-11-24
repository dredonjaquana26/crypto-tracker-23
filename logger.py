import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {'INFO': '\033[92m', 'ERROR': '\033[91m', 'WARNING': '\033[93m'}
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        timestamp = datetime.now().strftime('%H:%M:%S')
        return f"{color}[{timestamp}] {record.levelname}: {record.getMessage()}{self.RESET}"

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CryptoFormatter())
    logger.addHandler(handler)
    return logger

log = setup_logger('crypto-tracker-23')

def log_trade(action: str, pair: str, price: float):
    msg = f"Trade signal -> {action.upper()} {pair} @ {price:.2f} USD"
    log.info(msg)

def log_alert(condition: str):
    log.warning(f"Alert triggered: {condition}")