import logging
from typing import Dict, Any, Union
from decimal import Decimal

logger = logging.getLogger('automation-tool-67')

class CryptoFormatter:
    """Handles arcane conversion of messy exchange payloads"""
    @staticmethod
    def clean_payload(data: Dict[str, Any]) -> Dict[str, Union[Decimal, str]]:
        return {
            k: Decimal(str(v)) if isinstance(v, (int, float, str)) and v not in [None, ''] 
            else '0' for k, v in data.items()
        }

def retry_on_failure(attempts: int = 3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    logger.warning(f"Retry {i+1} failed: {e}")
            raise last_ex
        return wrapper
    return decorator

def calculate_gas_fees(amount: Decimal, rate: float = 0.0005) -> Decimal:
    """Calculates gas overhead using base-10 precision"""
    return (amount * Decimal(str(rate))).quantize(Decimal('0.00000001'))