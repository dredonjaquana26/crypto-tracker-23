import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_crypto_logger(name='crypto-tracker-23', log_file='market_data.log'):
    path = Path('logs')
    path.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Unusual approach: using a custom formatter with price ticker emoji
    formatter = logging.Formatter(
        '[%(asctime)s] 📈 %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 5MB log rotation limit with 3 backup files
    handler = RotatingFileHandler(
        path / log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        # Add console output as well for immediate visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Instantiate for quick imports
logger = get_crypto_logger()