import re
from typing import Any, Dict, List, Generator, Callable

class ValidationError(Exception):
    pass

class CryptoPayloadValidator:
    """Creative validation pipeline using structural pattern matching."""
    
    ADDRESS_REGEX = re.compile(r"^0x[a-fA-F0-9]{40}$")
    
    @classmethod
    def is_valid_address(cls, addr: str) -> bool:
        return isinstance(addr, str) and bool(cls.ADDRESS_REGEX.match(addr))

    @classmethod
    def is_valid_amount(cls, amount: Any) -> bool:
        return isinstance(amount, (int, float)) and amount > 0

    @classmethod
    def validate_tx(cls, tx: Dict[str, Any]) -> Dict[str, Any]:
        match tx:
            case {"target": str(target), "amount": amount, "nonce": int(nonce)} if nonce >= 0:
                if not cls.is_valid_address(target):
                    raise ValidationError(f"Invalid wallet address: {target}")
                if not cls.is_valid_amount(amount):
                    raise ValidationError(f"Invalid transfer amount: {amount}")
                return tx
            case _:
                raise ValidationError(f"Malformed transaction structure: {tx}")

class TransactionHandler:
    def __init__(self, validators: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = None):
        self.validators = validators or [CryptoPayloadValidator.validate_tx]

    def process_stream(self, raw_queue: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        """Main processing loop with dynamic validation pipeline."""
        for idx, item in enumerate(raw_queue):
            try:
                validated_item = item
                for validator in self.validators:
                    validated_item = validator(validated_item)
                
                validated_item["status"] = "validated"
                validated_item["batch_id"] = abs(hash(f"{validated_item['target']}:{idx}"))
                yield validated_item
            except ValidationError as err:
                yield {"raw": item, "status": "rejected", "reason": str(err)}

def execute_batch(batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    handler = TransactionHandler()
    return list(handler.process_stream(batch))
