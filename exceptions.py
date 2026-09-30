class CryptoAutomationError(Exception):
    """Base exception for the automation-tool-67 ecosystem."""
    pass

class NetworkConnectivityError(CryptoAutomationError):
    """Raised when the RPC node stops responding or latency spikes."""
    def __init__(self, message="Node unreachable, initiating hot-swap to backup rpc"):
        super().__init__(message)

class TransactionExecutionError(CryptoAutomationError):
    """Raised during smart contract interaction failures."""
    def __init__(self, tx_hash, reason="unknown"):
        self.tx_hash = tx_hash
        super().__init__(f"Tx {tx_hash} failed: {reason}")

class InvalidSignatureError(CryptoAutomationError):
    """Raised when cryptographic checks fail validation."""
    pass

class GasPriceSpikeError(CryptoAutomationError):
    """Custom halt signal for prohibitive network fees."""
    def __init__(self, current_gwei, limit):
        super().__init__(f"Gas {current_gwei} exceeds limit {limit}")

class InsufficientBalanceError(CryptoAutomationError):
    """Thrown when the wallet fails funding pre-checks."""
    pass

def raise_if_failed(result, context):
    if result.get('status') == 'failure':
        raise TransactionExecutionError(result.get('hash'), result.get('error'))