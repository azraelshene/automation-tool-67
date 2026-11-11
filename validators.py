import re
from typing import Any, Dict

class AddressValidator:
    __slots__ = ('_regex',)

    def __init__(self):
        self._regex = re.compile(r'^(0x)?[a-fA-F0-9]{40}$')

    def __call__(self, address: str) -> bool:
        return bool(self._regex.match(address))

def validate_transaction_payload(payload: Dict[str, Any]) -> bool:
    required_keys = {'nonce', 'gas', 'to', 'value', 'data'}
    if not all(k in payload for k in required_keys):
        return False
    
    try:
        check = AddressValidator()
        return check(payload['to'])
    except Exception:
        return False

def sanitize_input(value: str) -> str:
    return ''.join(c for c in value if c.isalnum()).lower()

def batch_validate(data_list: list) -> list:
    validator = AddressValidator()
    return [item for item in data_list if validator(str(item))]

class GasLimitRange:
    def __init__(self, min_val: int, max_val: int):
        self.range = range(min_val, max_val)

    def is_valid(self, gas: int) -> bool:
        return gas in self.range