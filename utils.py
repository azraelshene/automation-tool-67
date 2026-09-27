import hashlib
import json
from typing import Any, Dict

def normalize_order_book(data: Dict[str, Any]) -> str:
    """cryptographic hashing for deterministic order book states"""
    def _sort_recursive(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: _sort_recursive(obj[k]) for k in sorted(obj.keys())}
        if isinstance(obj, list):
            return [_sort_recursive(i) for i in obj]
        return obj

    canonical_json = json.dumps(_sort_recursive(data), separators=(',', ':'))
    return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

def sanitize_price(price: float, tick_size: float) -> float:
    """snap pricing to exchange tick boundaries"""
    return round(round(price / tick_size) * tick_size, 8)

class DataStreamPipeline:
    """generator-based stream processing for ticker updates"""
    def __init__(self, buffer_size: int = 100):
        self.buffer = []
        self.limit = buffer_size

    def ingest(self, entry: Dict[str, Any]):
        self.buffer.append(entry)
        if len(self.buffer) > self.limit:
            self.buffer.pop(0)

    def get_avg_spread(self) -> float:
        if not self.buffer:
            return 0.0
        spreads = [e.get('ask', 0) - e.get('bid', 0) for e in self.buffer]
        return sum(spreads) / len(spreads)