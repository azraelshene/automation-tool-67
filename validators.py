 """Validation utilities for cryptocurrency transaction payloads and network parameters."""

from typing import Callable, Any, Dict, Tuple, Pattern
import re

ValidatorFunc = Callable[[Any], Tuple[bool, str]]


class CryptoAddressValidator:
    """Rule-based address validator supporting EVM and Solana format checks."""

    EVM_PATTERN: Pattern[str] = re.compile(r"^0x[a-fA-F0-9]{40}$")
    SOLANA_PATTERN: Pattern[str] = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

    @classmethod
    def validate_evm(cls, address: str) -> Tuple[bool, str]:
        """Validate EVM hex checksum/address format."""
        if not isinstance(address, str):
            return False, "Address must be a string representation"
        if not cls.EVM_PATTERN.match(address):
            return False, "Invalid EVM hex address format"
        return True, "Valid EVM address"

    @classmethod
    def validate_solana(cls, address: str) -> Tuple[bool, str]:
        """Validate Base58 Solana public key address format."""
        if not isinstance(address, str):
            return False, "Address must be a string representation"
        if not cls.SOLANA_PATTERN.match(address):
            return False, "Invalid Solana Base58 address format"
        return True, "Valid Solana address"


def validate_gas_price(max_gwei: float = 500.0) -> ValidatorFunc:
    """Factory creating a gas price validator bounded by safety thresholds.

    Args:
        max_gwei: Maximum allowable gas price limit in Gwei.

    Returns:
        Validation function checking gas input against threshold.
    """
    def _check(val: Any) -> Tuple[bool, str]:
        try:
            numeric_val = float(val)
        except (ValueError, TypeError):
            return False, f"Gas price '{val}' cannot be parsed as float"

        if numeric_val <= 0:
            return False, "Gas price must be strictly positive"
        if numeric_val > max_gwei:
            return False, f"Gas price {numeric_val} exceeds limit of {max_gwei} Gwei"
        return True, "Gas price within acceptable range"

    return _check


def enforce_schema(data: Dict[str, Any], rules: Dict[str, ValidatorFunc]) -> Tuple[bool, Dict[str, str]]:
    """Validate a target dictionary against schema validation callbacks.

    Args:
        data: Target key-value payload to inspect.
        rules: Mapping of keys to validation callback functions.

    Returns:
        Tuple of overall validity flag and dictionary of specific failure messages.
    """
    errors: Dict[str, str] = {}
    for key, validator in rules.items():
        if key not in data:
            errors[key] = "Missing required payload parameter"
            continue
        is_valid, msg = validator(data[key])
        if not is_valid:
            errors[key] = msg
    return len(errors) == 0, errors
