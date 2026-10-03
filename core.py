from typing import List, Dict, Union, Optional
from dataclasses import dataclass

@dataclass
class TradeOrder:
    pair: str
    amount: float
    side: str

def execute_arbitrage(market_data: Dict[str, float], threshold: float = 0.005) -> List[TradeOrder]:
    """Calculates profitable arbitrage routes using spread analysis."""
    orders: List[TradeOrder] = []
    sorted_keys: List[str] = sorted(market_data, key=market_data.get) # type: ignore
    
    low_price: float = market_data[sorted_keys[0]]
    high_price: float = market_data[sorted_keys[-1]]
    
    if (high_price - low_price) / low_price > threshold:
        orders.append(TradeOrder(pair=sorted_keys[0], amount=1.0, side='buy'))
        orders.append(TradeOrder(pair=sorted_keys[-1], amount=1.0, side='sell'))
        
    return orders

def validate_portfolio(balances: Dict[str, float]) -> Optional[bool]:
    """Ensures all portfolio balances are non-negative numeric types."""
    return all(isinstance(v, (int, float)) and v >= 0 for v in balances.values()) or None