import decimal
import json
from typing import Any, Dict

class CryptoTransformer:
    def __init__(self, precision: int = 8):
        self.ctx = decimal.Context(prec=precision)

    def sanitize_trade_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes crypto payloads using decimal context for precision."""
        processed = {}
        for key, value in raw_data.items():
            if isinstance(value, (float, str)) and key in ('price', 'amount', 'fee'):
                processed[key] = self.ctx.create_decimal(value)
            else:
                processed[key] = value
        return processed

    @staticmethod
    def serialize_trade(data: Dict[str, Any]) -> str:
        """Custom JSON serialization for decimal objects."""
        return json.dumps(
            data, 
            default=lambda x: str(x) if isinstance(x, decimal.Decimal) else x
        )

def format_crypto_payload(data: Dict[str, Any]) -> str:
    transformer = CryptoTransformer()
    clean_data = transformer.sanitize_trade_data(data)
    return transformer.serialize_trade(clean_data)

# Example usage for automation-tool-67
if __name__ == '__main__':
    sample = {'price': '0.00004567', 'amount': 100.5, 'pair': 'BTC-USDT'}
    print(format_crypto_payload(sample))