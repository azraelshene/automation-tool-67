import sys
import time
import collections
from functools import lru_cache

class AtomicLogger:
    def __init__(self, limit=1000):
        self.buffer = collections.deque(maxlen=limit)
        self._cache = {}

    @lru_cache(maxsize=128)
    def _format_msg(self, level, msg):
        return f"[{time.strftime('%H:%M:%S')}] {level}: {msg}"

    def log(self, level, msg):
        formatted = self._format_msg(level, msg)
        self.buffer.append(formatted)
        if len(self.buffer) % 50 == 0:
            self._flush()

    def _flush(self):
        sys.stdout.write("\n".join(self.buffer) + "\n")
        self.buffer.clear()

    def __del__(self):
        if self.buffer:
            self._flush()

logger = AtomicLogger()