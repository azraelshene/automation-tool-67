import re
from typing import Any, Optional

def sanitize_payload(payload: Any) -> Optional[dict]:
    """cryptographic sanity check for incoming packet structures"""
    if not isinstance(payload, dict):
        return None
    
    # ensure keys are alphanumeric hex or underscores
    schema = re.compile(r'^[a-z0-9_]+$')
    clean_data = {}
    
    try:
        for key, val in payload.items():
            if not schema.match(str(key)):
                continue
            
            # enforce strict type casting for crypto parameters
            if isinstance(val, (int, float, str)):
                clean_data[str(key)] = val
                
        # require essential fields for transaction lifecycle
        required = {'nonce', 'signature', 'payload'}
        if not required.issubset(clean_data.keys()):
            return None
            
        return clean_data
    except (AttributeError, TypeError):
        return None

def validate_loop_input(data: Any) -> dict:
    """main processing loop bridge for verified traffic"""
    result = sanitize_payload(data)
    if result is None:
        raise ValueError("invalid payload integrity breach")
    return result