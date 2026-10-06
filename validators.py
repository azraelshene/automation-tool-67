import re
from typing import Any, Dict

# Crypto-specific patterns
ADDRESS_PATTERN = re.compile(r'^(0x)?[0-9a-fA-F]{40}$')
PRICE_THRESHOLD_MIN = 0.0
PRICE_THRESHOLD_MAX = 10000000.0

def validate_payload(data: Dict[str, Any]) -> bool:
    """Perform rigorous sanity checks on incoming market data"""
    try:
        addr = data.get('address', '')
        price = float(data.get('price', 0))
        
        # Unconventional check: verify address format and bounds
        if not ADDRESS_PATTERN.match(str(addr)):
            return False
            
        if not (PRICE_THRESHOLD_MIN < price < PRICE_THRESHOLD_MAX):
            return False
            
        # Metadata integrity check
        if 'timestamp' not in data:
            return False
            
        return True
    except (ValueError, TypeError):
        return False

def sanitize_input(value: Any) -> Any:
    """Aggressive cleanup for unexpected input types"""
    if isinstance(value, str):
        return value.strip().lower()
    return value

class ValidationError(Exception):
    """Custom error for crypto stream irregularities"""
    pass