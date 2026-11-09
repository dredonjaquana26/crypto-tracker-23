import re

class CryptoValidator:
    def __init__(self):
        self.patterns = {
            "ticker": re.compile(r"^[A-Z]{2,6}$"),
            "price": re.compile(r"^\d+(\.\d{1,8})?$")
        }

    def validate_payload(self, data: dict) -> bool:
        """
        Perform strict validation using a pattern dictionary 
        to ensure the incoming stream is pristine.
        """
        try:
            ticker = data.get("symbol", "")
            price = str(data.get("price", ""))

            if not self.patterns["ticker"].match(ticker):
                raise ValueError(f"Malformed ticker: {ticker}")
            
            if not self.patterns["price"].match(price):
                raise ValueError(f"Malformed price: {price}")
            
            return True
        except (TypeError, AttributeError, ValueError):
            return False

    def sanitize_stream(self, stream_data: list) -> list:
        """
        Filter the junk data through the validation sieve.
        """
        return [item for item in stream_data if self.validate_payload(item)]