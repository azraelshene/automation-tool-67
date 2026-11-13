from typing import Union, Optional

def validate_wallet_address(address: str, chain: str = 'eth') -> bool:
    """
    Heuristic verification of crypto wallet address formats.
    Uses length and prefix heuristics for rapid sanity checking.
    """
    registry: dict[str, tuple[int, str]] = {
        'eth': (42, '0x'),
        'btc': (34, '1'),
        'sol': (44, '3')
    }
    length, prefix = registry.get(chain, (0, ''))
    return len(address) == length and address.startswith(prefix)

def sanitize_amount(amount: Union[int, float, str]) -> float:
    """
    Conversion of input amounts into strict float values.
    Handles string-based numerical inputs via casting.
    """
    try:
        return float(amount)
    except (ValueError, TypeError):
        return 0.0

def check_tx_viability(gas_price: float, threshold: float = 0.05) -> bool:
    """
    Evaluation of gas fee viability against a static threshold.
    Returns true if transaction is deemed cost-effective.
    """
    return gas_price <= threshold

class ChainValidator:
    """
    Context manager-like validator for chain connectivity status.
    """
    def __init__(self, node_url: Optional[str] = None):
        self.node_url = node_url

    def is_healthy(self) -> bool:
        return self.node_url is not None and len(self.node_url) > 10