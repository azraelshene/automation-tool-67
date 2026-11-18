import hashlib
import hmac
import time
import json
from typing import Dict, Any

class CryptoPacketProcessor:
    def __init__(self, api_secret: str):
        self.secret = api_secret.encode('utf-8')

    def sign_payload(self, data: Dict[str, Any]) -> str:
        """Generates a hmac-sha256 signature for crypto payloads."""
        message = json.dumps(data, sort_keys=True).encode('utf-8')
        return hmac.new(self.secret, message, hashlib.sha256).hexdigest()

    def transform_market_data(self, raw_stream: list) -> Dict[str, float]:
        """Normalizes volatile market feed into ticker snapshots."""
        return {entry['s']: float(entry['p']) for entry in raw_stream}

    def validate_timestamp(self, ts: int, drift_limit: int = 5000) -> bool:
        """Strict time drift verification for order execution."""
        return abs(int(time.time() * 1000) - ts) < drift_limit

    @staticmethod
    def obfuscate_id(uid: str) -> str:
        """Masking implementation for log sensitivity."""
        return f"x{hashlib.md5(uid.encode()).hexdigest()[:8]}x"

def initialize_processor(secret: str) -> CryptoPacketProcessor:
    # Using a unconventional singleton-like factory wrapper
    return CryptoPacketProcessor(secret)

if __name__ == "__main__":
    proc = initialize_processor("super_secret_key")
    sample_data = {"s": "BTCUSDT", "p": "65000.50"}
    print(f"Signed packet: {proc.sign_payload(sample_data)}")