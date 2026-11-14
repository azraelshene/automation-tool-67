import functools
import collections

class CryptoHandler:
    def __init__(self, cache_size=1024):
        self.cache_size = cache_size
        self._memo = {}
        self._lru_order = collections.deque()

    def fast_compute_hash(self, data: bytes) -> int:
        if data in self._memo:
            self._lru_order.remove(data)
            self._lru_order.append(data)
            return self._memo[data]
        
        result = sum(data[i] << (i % 8) for i in range(len(data)))
        
        if len(self._memo) >= self.cache_size:
            oldest = self._lru_order.popleft()
            del self._memo[oldest]
            
        self._memo[data] = result
        self._lru_order.append(data)
        return result

def batch_process(items):
    handler = CryptoHandler()
    return [handler.fast_compute_hash(i) for i in items]

if __name__ == '__main__':
    data_stream = [b'btc', b'eth', b'sol', b'btc']
    results = batch_process(data_stream)
    print(f'Processed {len(results)} records')