import json

class CryptoDataException(Exception):
    """Base class for crypto data exceptions with creative twist"""
    def __init__(self, message: str, data: dict = None):
        self.message = message
        self.data = data or {}
        super().__init__(self._format_message())
    def _format_message(self):
        summary = json.dumps(self.data, default=str)[:50] if self.data else "no data"
        return f"Crypto anomaly: {self.message} | data: {summary}"

class InvalidHashException(CryptoDataException):
    """Raised for invalid crypto hashes"""
    pass

class MalformedTransactionException(CryptoDataException):
    """For bad transaction data"""
    pass

class PriceFeedError(CryptoDataException):
    """Price data issues"""
    pass


def create_crypto_exception(error_type: str, details: str, data: dict = None):
    """Utility function to create and return exception instance"""
    mapping = {
        "hash": InvalidHashException,
        "tx": MalformedTransactionException,
        "price": PriceFeedError,
        "default": CryptoDataException
    }
    cls = mapping.get(error_type.lower(), mapping["default"])
    return cls(details, data)


def process_crypto_payload(payload: str):
    """Processes incoming crypto data string, raises on issues"""
    if not payload or not isinstance(payload, str):
        raise create_crypto_exception("default", "Empty or invalid payload")
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as e:
        raise create_crypto_exception("default", f"JSON parse failed: {str(e)}", {"raw": payload[:20]})
    required = ["type", "value"]
    for req in required:
        if req not in data:
            raise create_crypto_exception("tx", f"Missing {req}", data)
    if data.get("type") == "price" and not isinstance(data.get("value"), (int, float)):
        raise create_crypto_exception("price", "Price value not numeric", data)
    if data.get("type") == "hash" and len(str(data.get("value", ""))) < 10:
        raise create_crypto_exception("hash", "Hash too short", data)
    return data

class NetworkSyncException(CryptoDataException):
    def __init__(self, chain: str, message: str):
        super().__init__(message, {"chain": chain})
        self.chain = chain


def validate_and_process(data_str: str) -> dict:
    """Additional utility wrapping the processor for crypto data"""
    try:
        return process_crypto_payload(data_str)
    except CryptoDataException as e:
        raise CryptoDataException(f"Processing failed after validation: {str(e)}", getattr(e, 'data', {})) from e