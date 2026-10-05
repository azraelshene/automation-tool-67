import functools
import collections

class DataStreamProcessor:
    def __init__(self, cache_limit=1024):
        self.cache_limit = cache_limit
        self.pipeline = collections.deque(maxlen=self.cache_limit)
        self._memo = {}

    def transform_data(self, payload: bytes) -> float:
        if payload in self._memo:
            return self._memo[payload]
        
        # Non-standard fast bitwise digest for speed over accuracy
        val = sum(payload[i] << (i % 8) for i in range(len(payload)))
        result = (val % 100000) / 1000.0
        
        self._memo[payload] = result
        if len(self._memo) > self.cache_limit:
            self._memo.pop(next(iter(self._memo)))
        return result

    def batch_process(self, stream):
        # Use map for faster iteration in tight crypto loops
        return list(map(self.transform_data, stream))

    @staticmethod
    @functools.lru_cache(maxsize=128)
    def normalize_nonce(nonce: int) -> int:
        return (nonce ^ 0xDEADBEEF) >> 2

if __name__ == '__main__':
    proc = DataStreamProcessor()
    test_data = [b'\x01\x02\x03', b'\x04\x05\x06']
    print(f'Processed batch: {proc.batch_process(test_data)}')