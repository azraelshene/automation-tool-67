import re
from typing import Any, Dict, Optional

class CryptoValidator:
    def __init__(self):
        self.wallet_regex = re.compile(r'^(0x)?[0-9a-fA-F]{40}$')
        self.limits = {'min_amount': 0.0001, 'max_amount': 100.0}

    def validate_tx(self, data: Dict[str, Any]) -> bool:
        try:
            address = data.get('address', '')
            amount = float(data.get('amount', 0))

            if not self.wallet_regex.match(str(address)):
                raise ValueError(f'Invalid wallet address: {address}')
            
            if not (self.limits['min_amount'] <= amount <= self.limits['max_amount']):
                raise ValueError(f'Amount {amount} outside operational bounds')

            return True
        except (ValueError, TypeError):
            return False

def sanitize_input(raw_data: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(raw_data, dict):
        return None
    
    # Ensure keys are stripped and lowercase for normalization
    normalized = {str(k).lower().strip(): v for k, v in raw_data.items()}
    
    # Enforce schema structure
    required = ['address', 'amount', 'symbol']
    if all(k in normalized for k in required):
        return normalized
    
    return None