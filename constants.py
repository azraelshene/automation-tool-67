"""Crypto network constants and dynamic unit lookup registry."""

from dataclasses import dataclass
from typing import Final, Mapping


class FrozenMeta(type):
    """Metaclass ensuring constant definitions remain immutable at runtime."""

    def __setattr__(cls, key: str, value: object) -> None:
        if hasattr(cls, key):
            raise AttributeError(f"Cannot reassign frozen constant '{key}'")
        super().__setattr__(key, value)


@dataclass(frozen=True)
class GasTier:
    low: int
    standard: int
    fast: int
    instant: int


class NetworkConstants(metaclass=FrozenMeta):
    CHAIN_IDS: Final[Mapping[str, int]] = {
        "ethereum": 1,
        "bsc": 56,
        "polygon": 137,
        "arbitrum": 42161,
        "optimism": 10,
    }

    DEFAULT_SLIPPAGE_BPS: Final[int] = 50
    MAX_APPROVAL_HEX: Final[str] = "0x" + "f" * 64

    GAS_TIERS: Final[Mapping[str, GasTier]] = {
        "ethereum": GasTier(low=15, standard=25, fast=40, instant=60),
        "polygon": GasTier(low=30, standard=50, fast=100, instant=200),
        "arbitrum": GasTier(low=1, standard=2, fast=3, instant=5),
    }

    @classmethod
    def gwei_to_wei(cls, gwei: float) -> int:
        return int(gwei * 10**9)

    @classmethod
    def get_chain_id(cls, name: str) -> int:
        key = name.lower().strip()
        if key not in cls.CHAIN_IDS:
            raise KeyError(f"Unsupported chain designation: '{name}'")
        return cls.CHAIN_IDS[key]