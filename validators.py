import re
from typing import Optional, Dict, Any

def validate_crypto_symbol(symbol: str) -> bool:
    if not isinstance(symbol, str):
        return False
    symbol = symbol.strip().upper()
    if len(symbol) < 2 or len(symbol) > 10:
        return False
    return symbol.isalpha()

def validate_address(crypto: str, address: str) -> bool:
    if not address or not isinstance(address, str):
        return False
    crypto = crypto.lower().strip()
    address = address.strip()
    if crypto == 'btc':
        if len(address) < 26 or len(address) > 35:
            return False
        pattern = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
        return bool(re.match(pattern, address))
    elif crypto == 'eth':
        if len(address) != 42 or not address.startswith('0x'):
            return False
        pattern = r'^0x[a-fA-F0-9]{40}$'
        return bool(re.match(pattern, address))
    elif crypto == 'sol':
        if len(address) < 32 or len(address) > 44:
            return False
        pattern = r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'
        return bool(re.match(pattern, address))
    return False

def validate_amount(amount: float, crypto: Optional[str] = None) -> bool:
    if not isinstance(amount, (int, float)):
        return False
    if amount <= 0:
        return False
    if crypto and crypto.lower() == 'btc' and amount < 0.00000001:
        return False
    return True

def validate_price(price: float) -> bool:
    if not isinstance(price, (int, float)) or price <= 0:
        return False
    return True

class ValidationManager:
    def __init__(self):
        self.rules: Dict[str, Any] = {}
    def add_rule(self, name: str, func: Any) -> None:
        self.rules[name] = func
    def validate_all(self, data: Dict[str, Any]) -> bool:
        for name, func in self.rules.items():
            if name in data and not func(data[name]):
                return False
        return True

def get_default_validator() -> ValidationManager:
    vm = ValidationManager()
    vm.add_rule('symbol', validate_crypto_symbol)
    vm.add_rule('amount', validate_amount)
    vm.add_rule('price', validate_price)
    return vm