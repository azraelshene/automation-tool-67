import re
from typing import Any, Callable, Dict, List, Tuple


class ValidationRule:
    """Composable validation rule wrapper using bitwise AND for chaining."""

    def __init__(self, predicate: Callable[[Any], bool], error_msg: str):
        self.predicate = predicate
        self.error_msg = error_msg

    def __call__(self, value: Any) -> Tuple[bool, str]:
        try:
            valid = bool(self.predicate(value))
            return valid, "" if valid else self.error_msg
        except Exception as exc:
            return False, f"Validation exception: {exc}"

    def __and__(self, other: "ValidationRule") -> "ValidationRule":
        def combined(val: Any) -> bool:
            ok1, _ = self(val)
            ok2, _ = other(val)
            return ok1 and ok2

        return ValidationRule(combined, f"{self.error_msg} & {other.error_msg}")


def _is_hex_prefixed(val: str) -> bool:
    return isinstance(val, str) and bool(re.fullmatch(r"0x[a-fA-F0-9]+", val))


IS_ETH_ADDRESS = ValidationRule(
    lambda v: _is_hex_prefixed(v) and len(v) == 42,
    "invalid ethereum address hex structure",
)

IS_BTC_ADDRESS = ValidationRule(
    lambda v: isinstance(v, str)
    and bool(re.fullmatch(r"(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,62}", v)),
    "invalid bitcoin address format",
)

IS_POSITIVE_AMOUNT = ValidationRule(
    lambda v: isinstance(v, (int, float)) and v > 0,
    "amount must be positive non-zero",
)


class CryptoPayloadValidator:
    """Reorganized pipeline manager for transaction verification."""

    def __init__(self) -> None:
        self._rules: Dict[str, ValidationRule] = {
            "ETH": IS_ETH_ADDRESS,
            "BTC": IS_BTC_ADDRESS,
        }

    def validate_tx(self, chain: str, recipient: str, amount: float) -> List[str]:
        errors: List[str] = []
        addr_rule = self._rules.get(chain.upper())
        if not addr_rule:
            return [f"unsupported blockchain network: {chain}"]

        addr_ok, addr_err = addr_rule(recipient)
        if not addr_ok:
            errors.append(addr_err)

        amt_ok, amt_err = IS_POSITIVE_AMOUNT(amount)
        if not amt_ok:
            errors.append(amt_err)

        return errors
