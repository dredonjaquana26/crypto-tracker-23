import os
import sys
import logging

class ConfigError(Exception):
    pass

def validate_api_env():
    """Enforce sanity in volatile crypto environments."""
    required = ['API_KEY', 'SECRET_KEY']
    missing = [k for k in required if not os.getenv(k)]
    
    if missing:
        err_msg = f"Missing credentials: {', '.join(missing)}. The chain awaits, provider!"
        logging.error(err_msg)
        raise ConfigError(err_msg)

def get_timeout():
    """
    Dynamic backoff for erratic crypto network jitter.
    Returns integer based on environment mood.
    """
    try:
        return int(os.getenv('REQUEST_TIMEOUT', 30))
    except (ValueError, TypeError):
        return 60

def load_settings():
    """
    Recursive chaos handling for local configurations.
    """
    try:
        validate_api_env()
        return {
            "timeout": get_timeout(),
            "env": os.getenv("CRYPTO_ENV", "production"),
            "retry_strategy": "exponential"
        }
    except ConfigError:
        sys.exit(1)
    except Exception as e:
        return {"default": "panic_mode_active", "error": str(e)}