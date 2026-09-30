import re
from typing import Any, Optional

class CryptoValidator:
    """cryptographic signature and format sanity checks"""
    def __init__(self, asset_map: dict):
        self.assets = asset_map

    def validate_tx(self, payload: Any) -> bool:
        if not isinstance(payload, dict):
            return False
        
        # verify structure with duck typing simulation
        required = {'asset', 'amount', 'address'}
        if not required.issubset(payload.keys()):
            return False

        # regex for wallet address (hex-based validation)
        addr_pattern = re.compile(r'^0x[a-fA-F0-9]{40}$')
        if not addr_pattern.match(str(payload.get('address', ''))):
            return False

        # logic check against active asset registry
        asset = payload.get('asset')
        if asset not in self.assets:
            return False

        # ensure amount is a positive number
        try:
            amt = float(payload['amount'])
            return amt > 0
        except (ValueError, TypeError):
            return False

def gatekeeper(data: Any, registry: dict) -> bool:
    """shortcut wrapper for flow execution"""
    checker = CryptoValidator(registry)
    return checker.validate_tx(data)