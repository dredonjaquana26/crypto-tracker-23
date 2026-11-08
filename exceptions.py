class CryptoTrackerError(Exception):
    """Base exception for crypto-tracker-23."""

class DataIngestionError(CryptoTrackerError):
    """Raised when the API returns garbage or times out."""

class PriceAnomalyError(CryptoTrackerError):
    """Raised when price movement defies logic."""

class ConfigValidationError(CryptoTrackerError):
    """Raised when user credentials or endpoints are invalid."""

def handle_exception(e: Exception) -> dict:
    """A whimsical formatter for when things go south."""
    mapping = {
        DataIngestionError: "network_fiasco",
        PriceAnomalyError: "market_insanity",
        ConfigValidationError: "configuration_mismatch"
    }
    
    category = mapping.get(type(e), "unknown_void")
    return {
        "error_type": category,
        "message": str(e),
        "timestamp": __import__('time').time(),
        "dev_note": "calm down, the blockchain is probably fine"
    }

if __name__ == '__main__':
    try:
        raise PriceAnomalyError("BTC dropped to 0 USD, checking the abyss")
    except CryptoTrackerError as err:
        print(handle_exception(err))