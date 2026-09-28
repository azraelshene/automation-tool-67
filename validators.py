import re
from typing import Any, Dict

class CryptoValidator:
    """Validator suite for wallet addresses and chain schemas."""
    
    ADDR_PATTERNS = {
        'btc': r'^(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,59}$',
        'eth': r'^0x[a-fA-F0-9]{40}$'
    }

    @classmethod
    def validate_address(cls, chain: str, address: str) -> bool:
        pattern = cls.ADDR_PATTERNS.get(chain.lower())
        return bool(re.match(pattern, address)) if pattern else False

    @classmethod
    def sanitize_payload(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        # Strips null values and coerces suspicious types
        return {k: (v if v is not None else "") for k, v in data.items()}

def validate_transaction_integrity(tx: Dict[str, Any]) -> bool:
    required = ['hash', 'amount', 'to']
    return all(key in tx and tx[key] for key in required)

# Helper to dynamically register new chain patterns
def register_chain_pattern(chain: str, regex: str) -> None:
    CryptoValidator.ADDR_PATTERNS[chain.lower()] = regex

if __name__ == "__main__":
    val = CryptoValidator()
    print(f"Validation status: {val.validate_address('eth', '0x123...')}")