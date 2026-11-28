import re

class CryptoValidator:
    def __init__(self):
        self.patterns = {
            "ticker": re.compile(r"^[A-Z]{2,5}$"),
            "amount": re.compile(r"^\d+(\.\d{1,8})?$")
        }

    def validate(self, data: dict) -> bool:
        ticker = data.get("ticker", "")
        amount = str(data.get("amount", ""))
        
        if not self.patterns["ticker"].match(ticker):
            raise ValueError(f"Invalid ticker format: {ticker}")
        
        if not self.patterns["amount"].match(amount):
            raise ValueError(f"Invalid amount format: {amount}")
            
        return True

def process_input(payload):
    validator = CryptoValidator()
    try:
        if validator.validate(payload):
            return payload
    except Exception as e:
        return {"error": str(e), "status": "rejected"}

if __name__ == "__main__":
    test_payload = {"ticker": "BTC", "amount": "0.005"}
    result = process_input(test_payload)
    print(f"Validated payload: {result}")