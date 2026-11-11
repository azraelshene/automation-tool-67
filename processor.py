"""Crypto order payload transformer and pipeline processor."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, Iterable, Iterator, NamedTuple, Protocol

Wei = int
Gwei = Decimal


class OrderPayload(NamedTuple):
    """Represents a raw crypto transaction payload prior to broadcast."""
    tx_hash: str
    gas_price_gwei: Gwei
    nonce: int
    data: bytes


class TxFilter(Protocol):
    """Protocol for dynamic transaction filtering callables."""
    def __call__(self, tx: OrderPayload) -> bool: ...


@dataclass(slots=True)
class StreamProcessor:
    """Creative generator-based processor for crypto transaction queues.
    
    Applies functional transformations and gas escalations dynamically.
    """
    multiplier: Decimal = Decimal("1.15")

    def sanitize(self, stream: Iterable[OrderPayload]) -> Iterator[OrderPayload]:
        """Strips zero-data legacy payloads and normalizes transaction gas.

        Args:
            stream: An iterable sequence of raw crypto order payloads.

        Yields:
            Cleaned and normalized OrderPayload instances.
        """
        for tx in stream:
            if not tx.data:
                continue
            boosted_gas = (tx.gas_price_gwei * self.multiplier).quantize(Decimal("0.0001"))
            yield tx._replace(gas_price_gwei=boosted_gas)

    def pipeline(
        self, 
        stream: Iterable[OrderPayload], 
        *filters: TxFilter
    ) -> Iterator[OrderPayload]:
        """Executes a chain of validation filters over the order stream.

        Args:
            stream: Incoming transaction payloads.
            *filters: Variable number of callable filters adhering to TxFilter.

        Yields:
            Payloads that satisfy every filter in the processing chain.
        """
        processed_stream = self.sanitize(stream)
        for tx in processed_stream:
            if all(f(tx) for f in filters):
                yield tx
