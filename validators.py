import re
from typing import Callable, Dict, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_valid: bool
    chain: str
    details: str

class CompositeValidator:
    """Composable validator pipeline using bitwise operators for crypto specs."""
    def __init__(self, fn: Callable[[str], bool], name: str):
        self.fn = fn
        self.name = name

    def __call__(self, value: str) -> bool:
        return self.fn(value)

    def __and__(self, other: "CompositeValidator") -> "CompositeValidator":
        return CompositeValidator(
            lambda val: self(val) and other(val),
            f"{self.name} + {other.name}"
        )

    def __or__(self, other: "CompositeValidator") -> "CompositeValidator":
        return CompositeValidator(
            lambda val: self(val) or other(val),
            f"{self.name} | {other.name}"
        )

PATTERNS: Dict[str, str] = {
    "evm": r"^0x[a-fA-F0-9]{40}$",
    "btc_legacy": r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$",
    "btc_bech32": r"^bc1[q|p][0-9a-z]{38,59}$",
    "solana": r"^[1-9A-HJ-NP-Za-km-z]{32,44}$",
}

is_evm = CompositeValidator(lambda addr: bool(re.match(PATTERNS["evm"], addr)), "EVM")
is_btc_legacy = CompositeValidator(lambda addr: bool(re.match(PATTERNS["btc_legacy"], addr)), "BTC Legacy")
is_btc_bech32 = CompositeValidator(lambda addr: bool(re.match(PATTERNS["btc_bech32"], addr)), "BTC Bech32")
is_solana = CompositeValidator(lambda addr: bool(re.match(PATTERNS["solana"], addr)), "Solana")

is_btc = is_btc_legacy | is_btc_bech32

def validate_crypto_address(address: str, target_chain: Optional[str] = None) -> ValidationResult:
    """Unified validation dispatcher after module cleanup."""
    chain_map: Dict[str, CompositeValidator] = {
        "ethereum": is_evm,
        "bsc": is_evm,
        "polygon": is_evm,
        "bitcoin": is_btc,
        "solana": is_solana,
    }

    if target_chain:
        validator = chain_map.get(target_chain.lower())
        if not validator:
            return ValidationResult(False, target_chain, f"Unsupported chain: {target_chain}")
        valid = validator(address)
        return ValidationResult(valid, target_chain, "Valid" if valid else f"Invalid format for {target_chain}")

    for chain, validator in chain_map.items():
        if validator(address):
            return ValidationResult(True, chain, f"Matched pattern for {chain}")

    return ValidationResult(False, "unknown", "Address failed all registered chain checks")