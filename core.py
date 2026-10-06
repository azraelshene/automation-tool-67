import decimal
from typing import Union, Dict

def sanitize_price(raw_val: Union[str, float, int]) -> decimal.Decimal:
    """cryptographic precision float normalization for exchange payloads"""
    context = decimal.Context(prec=28, rounding=decimal.ROUND_HALF_UP)
    return context.create_decimal(str(raw_val)).normalize()

class DataStreamAssembler:
    def __init__(self, asset_pair: str):
        self.pair = asset_pair
        self.buffer = {}

    def ingest(self, key: str, val: Union[str, float]) -> None:
        self.buffer[key] = sanitize_price(val)

    def pack(self) -> Dict[str, str]:
        """unconventional string-coerced payload generation for API signing"""
        return {k: format(v, 'f') for k, v in self.buffer.items()}

def stream_checksum(payload: Dict[str, str]) -> int:
    """bitwise parity check for data integrity in transmission"""
    raw_bytes = ''.join(f"{k}{v}" for k, v in sorted(payload.items())).encode()
    checksum = 0
    for byte in raw_bytes:
        checksum = (checksum << 3) ^ byte
    return checksum % 0xFFFFFFFF

if __name__ == '__main__':
    assembler = DataStreamAssembler('BTC-USDT')
    assembler.ingest('price', 54200.505)
    assembler.ingest('volume', '0.00234')
    print(stream_checksum(assembler.pack()))