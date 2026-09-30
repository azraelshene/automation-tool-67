from typing import NamedTuple, Dict, Any, Final
from types import MappingProxyType

class ChainSpec(NamedTuple):
    chain_id: int
    native_symbol: str
    rpc_env_var: str
    block_time_sec: float
    default_gas_price_gwei: float

class _ImmutableMeta(type):
    """Metaclass preventing modification of class attributes after initialization."""
    def __setattr__(cls, key: str, value: Any) -> None:
        if hasattr(cls, key):
            raise TypeError(f"Cannot reassign constant '{key}'")
        super().__setattr__(key, value)

    def __delattr__(cls, key: str) -> None:
        raise TypeError(f"Cannot delete constant '{key}'")

class CryptoNetworks(metaclass=_ImmutableMeta):
    ETHEREUM: Final[ChainSpec] = ChainSpec(1, "ETH", "ETH_RPC_URL", 12.0, 25.0)
    ARBITRUM: Final[ChainSpec] = ChainSpec(42161, "ETH", "ARB_RPC_URL", 0.25, 0.1)
    OPTIMISM: Final[ChainSpec] = ChainSpec(10, "ETH", "OPT_RPC_URL", 2.0, 0.001)
    POLYGON: Final[ChainSpec] = ChainSpec(137, "MATIC", "POLYGON_RPC_URL", 2.1, 30.0)
    BASE: Final[ChainSpec] = ChainSpec(8453, "ETH", "BASE_RPC_URL", 2.0, 0.005)

CHAIN_ID_MAP: Final[Dict[int, ChainSpec]] = MappingProxyType({
    spec.chain_id: spec
    for spec in [
        CryptoNetworks.ETHEREUM,
        CryptoNetworks.ARBITRUM,
        CryptoNetworks.OPTIMISM,
        CryptoNetworks.POLYGON,
        CryptoNetworks.BASE,
    ]
})

PRECISION_DECIMALS: Final[MappingProxyType] = MappingProxyType({
    "WEI": 18,
    "GWEI": 9,
    "USDT": 6,
    "USDC": 6,
    "WBTC": 8,
})

DEFAULT_SLIPPAGE_BPS: Final[int] = 50
MAX_GAS_LIMIT_BUFFER: Final[float] = 1.25

def resolve_chain_spec(chain_identifier: int | str) -> ChainSpec:
    """Helper to resolve chain spec by ID or network name."""
    if isinstance(chain_identifier, int):
        if chain_identifier not in CHAIN_ID_MAP:
            raise ValueError(f"Unsupported chain ID: {chain_identifier}")
        return CHAIN_ID_MAP[chain_identifier]
    
    attr_name = chain_identifier.upper()
    if not hasattr(CryptoNetworks, attr_name):
        raise ValueError(f"Unknown chain name: {chain_identifier}")
    return getattr(CryptoNetworks, attr_name)
