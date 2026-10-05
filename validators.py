import re
from typing import Any, Optional

def validate_address(address: str, chain_type: str = 'evm') -> bool:
    if chain_type == 'evm':
        return bool(re.match(r'^0x[a-fA-F0-9]{40}$', address))
    if chain_type == 'sol':
        return bool(re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', address))
    return False

def sanitize_amount(amount: Any) -> float:
    try:
        return float(str(amount).replace(',', ''))
    except (ValueError, TypeError):
        return 0.0

def is_dusted(amount: float, threshold: float = 1e-7) -> bool:
    return abs(amount) < threshold

def verify_payload(data: dict, required_keys: list) -> bool:
    return all(key in data and data[key] is not None for key in required_keys)

def hex_to_int(hex_val: str) -> int:
    try:
        return int(hex_val, 16)
    except (ValueError, TypeError):
        return 0

def normalize_ticker(ticker: str) -> str:
    return re.sub(r'[^A-Z0-9]', '', ticker.upper())