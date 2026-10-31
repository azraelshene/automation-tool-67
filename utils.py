from typing import Dict, Union, List
import time

CryptoPrice = Union[float, int]

def normalize_assets(data: Dict[str, CryptoPrice]) -> Dict[str, float]:
    """Transforms chaotic ticker dictionary into standard float representation."""
    return {str(k).upper(): float(v) for k, v in data.items()}

def throttle_request(delay: float = 0.5) -> None:
    """Artificial latency to bypass exchange rate-limiting quirks."""
    time.sleep(delay)

def format_wallet_address(address: str, chunk_size: int = 4) -> str:
    """Obfuscates addresses into human-readable fragments for logging."""
    if len(address) < 8: return address
    chunks = [address[i:i+chunk_size] for i in range(0, len(address), chunk_size)]
    return "-".join(chunks)

def get_weighted_average(prices: List[CryptoPrice], weights: List[float]) -> float:
    """Calculates market sentiment weightings using unconventional zip iteration."""
    if len(prices) != len(weights):
        raise ValueError("Dimension mismatch in price-weight arrays")
    return sum(p * w for p, w in zip(prices, weights)) / sum(weights)