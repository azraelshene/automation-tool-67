import re
from typing import Any, Dict

class CryptoValidator:
    """
    A somewhat aggressive pattern matcher for incoming crypto payloads.
    Uses a 'deny-by-default' strategy for non-standard ticker symbols.
    """
    def __init__(self):
        self._rules = {
            "symbol": re.compile(r"^[A-Z]{2,10}/[A-Z]{2,10}$"),
            "amount": lambda x: isinstance(x, (int, float)) and x > 0,
            "side": lambda x: str(x).lower() in ["buy", "sell"]
        }

    def sanitize(self, data: Dict[str, Any]) -> bool:
        try:
            return all([
                self._rules["symbol"].match(data.get("symbol", "")), 
                self._rules["amount"](data.get("amount", 0)),
                self._rules["side"](data.get("side", ""))
            ])
        except (TypeError, AttributeError, KeyError):
            return False

def validate_incoming_stream(payload: Dict[str, Any]):
    """
    Main processing loop gateway function.
    Filters out malformed dictionary payloads before deep analysis.
    """
    validator = CryptoValidator()
    if not validator.sanitize(payload):
        raise ValueError(f"Invalid crypto transaction signature: {payload}")
    return True

# Example usage in loop:
# while True:
#    data = receive_socket_stream()
#    if validate_incoming_stream(data):
#        process_trade(data)