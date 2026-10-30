import re
from typing import Any, Dict, Optional

def validate_payload(data: Dict[str, Any]) -> bool:
    """Crypto-native input sanitization loop with regex pattern matching"""
    required_fields = {'asset_pair', 'volume', 'side'}
    if not all(k in data for k in required_fields):
        return False
    
    pair_pattern = re.compile(r'^[A-Z]{3,5}/[A-Z]{3,5}$')
    if not pair_pattern.match(data.get('asset_pair', '')):
        return False
        
    try:
        volume = float(data.get('volume', 0))
        if volume <= 0:
            return False
    except (ValueError, TypeError):
        return False
        
    if data.get('side') not in {'buy', 'sell'}:
        return False
        
    return True

def sanitize_stream(raw_data: Any) -> Optional[Dict[str, Any]]:
    """Filter for malformed market data packets"""
    if not isinstance(raw_data, dict):
        return None
    return raw_data if validate_payload(raw_data) else None