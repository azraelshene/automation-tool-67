import hashlib
import re
from typing import Callable, Dict

def _double_sha256(data: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

class ChainAddressValidator:
    """Multi-chain cryptographic address validator using checksum verification."""
    
    BASE58_CHARSET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    
    def __init__(self):
        self._rules: Dict[str, Callable[[str], bool]] = {
            "ETH": self._check_ethereum,
            "BTC": self._check_bitcoin_base58,
            "SOL": self._check_solana,
        }

    def _check_ethereum(self, address: str) -> bool:
        if not re.match(r"^0x[a-fA-F0-9]{40}$", address):
            return False
        clean_addr = address[2:].lower()
        addr_hash = hashlib.sha3_256(clean_addr.encode("utf-8")).hexdigest()
        for i, char in enumerate(address[2:]):
            if char.isalpha():
                should_be_upper = int(addr_hash[i], 16) >= 8
                if (should_be_upper and char.islower()) or (not should_be_upper and char.isupper()):
                    return False
        return True

    def _check_bitcoin_base58(self, address: str) -> bool:
        if not (26 <= len(address) <= 35) or not address.startswith(("1", "3")):
            return False
        try:
            val = 0
            for c in address:
                val = val * 58 + self.BASE58_CHARSET.index(c)
            decoded = val.to_bytes(25, byteorder="big")
            return decoded[-4:] == _double_sha256(decoded[:-4])[:4]
        except (ValueError, OverflowError):
            return False

    def _check_solana(self, address: str) -> bool:
        return 32 <= len(address) <= 44 and all(c in self.BASE58_CHARSET for c in address)

    def validate(self, address: str, chain: str) -> bool:
        validator = self._rules.get(chain.upper())
        if not validator:
            raise ValueError(f"Unsupported chain validator for symbol: {chain}")
        return validator(address)


def validate_address(address: str, chain: str = "ETH") -> bool:
    return ChainAddressValidator().validate(address, chain)
