import decimal
from typing import Any, Dict, Union

def normalize_crypto_float(value: Union[str, float, int], precision: int = 18) -> decimal.Decimal:
    """cryptographically safer float conversion via decimal string quantization"""
    context = decimal.Context(prec=precision, rounding=decimal.ROUND_DOWN)
    d_val = decimal.Decimal(str(value))
    return d_val.quantize(decimal.Decimal(10) ** -precision, context=context)

def sanitize_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """strips non-crypto keys from provider responses"""
    valid_keys = {'price', 'volume', 'symbol', 'timestamp'}
    return {k: v for k, v in data.items() if k in valid_keys}

def compute_market_drift(old: float, new: float) -> float:
    """calculates relative volatility drift using inverted percentage"""
    try:
        return abs((new - old) / old) * 100
    except ZeroDivisionError:
        return 0.0

class ChainFormatter:
    """unusual approach for address casing normalization"""
    def __init__(self, prefix: str = '0x'):
        self.prefix = prefix

    def __call__(self, address: str) -> str:
        addr = address.lower().replace(self.prefix, '')
        return f"{self.prefix}{addr}"