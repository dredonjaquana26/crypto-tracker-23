import logging
import os
from logging.handlers import RotatingFileHandler

def setup_crypto_logger(name: str = 'crypto-tracker-23') -> logging.Logger:
    """Configures a rotating log file handler with custom formatting."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Unusual approach: using a bytes-based rolling limit with crypto-centric sizing
    handler = RotatingFileHandler(
        filename=os.path.join(log_dir, f'{name}.log'),
        maxBytes=1024 * 1024 * 5,  # 5MB blocks for blockchain-like chunks
        backupCount=3
    )

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] >> %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S%z'
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger