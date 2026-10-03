import struct
from typing import Any, Dict, Iterator, List, Tuple


class BinaryTradeProcessor:
    """Zero-copy binary trade payload parser with streaming state updates."""

    # Format: 8B timestamp (ms), 4B price (*10^4), 4B volume (*10^4), 1B side flag
    STRUCT_FMT = "!QIIB"
    PAYLOAD_LEN = struct.calcsize(STRUCT_FMT)

    def __init__(self, smoothing_factor: float = 0.2):
        self.alpha = smoothing_factor
        self.last_ema: float | None = None
        self.accumulated_volume: float = 0.0

    def parse_raw_stream(self, buffer: bytes) -> Iterator[Dict[str, Any]]:
        """Parses raw buffer using memoryview for zero-copy slicing."""
        mem = memoryview(buffer)
        for offset in range(0, len(mem) - self.PAYLOAD_LEN + 1, self.PAYLOAD_LEN):
            ts, price_i, vol_i, side_b = struct.unpack_from(self.STRUCT_FMT, mem, offset)
            yield {
                "timestamp": ts,
                "price": price_i / 10000.0,
                "volume": vol_i / 10000.0,
                "is_buy": bool(side_b & 0x01),
            }

    def compute_ema_stream(
        self, trades: Iterator[Dict[str, Any]]
    ) -> Iterator[Tuple[Dict[str, Any], float]]:
        """Generator processing price updates and dynamic exponential moving average."""
        for trade in trades:
            price = trade["price"]
            if self.last_ema is None:
                self.last_ema = price
            else:
                self.last_ema = (self.alpha * price) + ((1.0 - self.alpha) * self.last_ema)

            self.accumulated_volume += trade["volume"]
            trade["total_vol"] = round(self.accumulated_volume, 4)
            yield trade, round(self.last_ema, 4)


def process_crypto_buffer(data: bytes, alpha: float = 0.15) -> List[Tuple[Dict[str, Any], float]]:
    """Utility wrapper for ingesting and transforming raw socket buffers."""
    processor = BinaryTradeProcessor(smoothing_factor=alpha)
    stream = processor.parse_raw_stream(data)
    return list(processor.compute_ema_stream(stream))
