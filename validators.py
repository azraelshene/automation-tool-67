import functools
import time

class ValidatorCache:
    _data = {}
    _expiry = {}

    @classmethod
    def memoize_validation(cls, ttl=30):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (func.__name__, args, frozenset(kwargs.items()))
                now = time.time()
                if key in cls._data and now < cls._expiry.get(key, 0):
                    return cls._data[key]
                result = func(*args, **kwargs)
                cls._data[key] = result
                cls._expiry[key] = now + ttl
                return result
            return wrapper
        return decorator

@ValidatorCache.memoize_validation(ttl=60)
def validate_tx_signature(tx_hash: str, sig: str) -> bool:
    # Simulate high-latency crypto signature validation
    time.sleep(0.5)
    return len(tx_hash) == 64 and len(sig) > 128

def batch_validate(transactions: list) -> list:
    # Vectorized check approach using local cache
    return [validate_tx_signature(t['hash'], t['sig']) for t in transactions]

def clean_stale_cache():
    now = time.time()
    expired = [k for k, v in ValidatorCache._expiry.items() if now > v]
    for k in expired:
        ValidatorCache._data.pop(k, None)
        ValidatorCache._expiry.pop(k, None)