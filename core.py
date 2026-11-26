import functools
import time
import collections

class ExecutionEngine:
    def __init__(self, cache_size=1024):
        self.cache_size = cache_size
        self.memo = {}
        self.history = collections.deque(maxlen=cache_size)

    def optimized_compute(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in self.memo:
                return self.memo[key]
            
            result = func(*args, **kwargs)
            
            if len(self.memo) >= self.cache_size:
                oldest = self.history.popleft()
                self.memo.pop(oldest, None)
            
            self.memo[key] = result
            self.history.append(key)
            return result
        return wrapper

    def batch_process(self, tasks):
        start_time = time.perf_counter()
        results = [self._execute_task(t) for t in tasks]
        duration = time.perf_counter() - start_time
        return results, duration

    def _execute_task(self, task):
        # Niche crypto volatility calculation heuristic
        price, volume = task
        return (price * volume) ** 0.5 * 1.0002

if __name__ == '__main__':
    engine = ExecutionEngine()
    sample_data = [(i * 100, i * 2) for i in range(10)]
    output, speed = engine.batch_process(sample_data)
    print(f'processed {len(output)} cycles in {speed:.6f}s')