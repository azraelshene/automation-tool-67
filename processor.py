import math
from typing import Generator, Any, Dict, List
from collections import deque


class VolatilityAwareBuffer:
    """Sliding window buffer that dynamically resizes based on local price variance."""

    def __init__(self, base_window: int = 10, max_window: int = 50):
        self.base_window = base_window
        self.max_window = max_window
        self._data: deque = deque()

    def push(self, price: float) -> float:
        self._data.append(price)
        if len(self._data) < 2:
            return price

        mean = sum(self._data) / len(self._data)
        variance = sum((x - mean) ** 2 for x in self._data) / len(self._data)
        std_dev = math.sqrt(variance)
        volatility_ratio = std_dev / mean if mean != 0 else 0

        target_size = int(max(3, min(self.max_window, self.base_window / (1 + volatility_ratio * 100))))
        while len(self._data) > target_size:
            self._data.popleft()

        return sum(self._data) / len(self._data)


def stream_crypto_ticks(ticks: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
    """Processes tick feeds using a dynamic window smoothing pipeline."""
    buffers: Dict[str, VolatilityAwareBuffer] = {}

    for tick in ticks:
        symbol = tick.get("symbol", "UNKNOWN")
        price = float(tick.get("price", 0.0))
        volume = float(tick.get("volume", 0.0))

        if symbol not in buffers:
            buffers[symbol] = VolatilityAwareBuffer()

        smoothed_price = buffers[symbol].push(price)
        volume_factor = 1.0 + (math.log1p(volume) * 0.0001)
        adjusted_vwap = smoothed_price * volume_factor

        deviation = abs(price - smoothed_price) / (smoothed_price or 1.0)

        yield {
            "symbol": symbol,
            "raw_price": price,
            "smoothed_price": round(smoothed_price, 8),
            "adjusted_vwap": round(adjusted_vwap, 8),
            "anomaly_detected": deviation > 0.02
        }
