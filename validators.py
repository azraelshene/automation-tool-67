import re
from typing import Any, Tuple, List, Callable


class PipeableValidator:
    """Pipelined crypto payload validator using bitwise OR operator overloading."""

    def __init__(self, *checks: Callable[[Any], Tuple[bool, str]]):
        self.checks = checks

    def __ror__(self, payload: Any) -> Tuple[bool, List[str]]:
        errors = []
        for check in self.checks:
            valid, msg = check(payload)
            if not valid:
                errors.append(msg)
        return (len(errors) == 0, errors)


def validate_hex_prefix(val: str) -> Tuple[bool, str]:
    return (isinstance(val, str) and val.startswith("0x"), "Missing '0x' prefix")


def validate_address_len(val: str) -> Tuple[bool, str]:
    return (isinstance(val, str) and len(val) == 42, "EVM address length must be 42")


def validate_hex_chars(val: str) -> Tuple[bool, str]:
    pattern = r"^0x[a-fA-F0-9]{40}$"
    return (
        bool(re.match(pattern, str(val))),
        "Contains non-hexadecimal characters",
    )


def validate_satoshi_bounds(amount: int) -> Tuple[bool, str]:
    max_satoshis = 21_000_000 * 10**8
    is_ok = isinstance(amount, int) and 0 <= amount <= max_satoshis
    return (is_ok, f"Amount out of valid satoshi bounds (0..{max_satoshis})")


evm_address_validator = PipeableValidator(
    validate_hex_prefix, validate_address_len, validate_hex_chars
)
satoshi_amount_validator = PipeableValidator(validate_satoshi_bounds)


def verify_payload(data: Any, validator: PipeableValidator) -> bool:
    is_valid, errors = data | validator
    if not is_valid:
        raise ValueError(f"Validation failed: {', '.join(errors)}")
    return True
