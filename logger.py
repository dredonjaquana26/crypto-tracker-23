import time
from functools import lru_cache

class AsyncLogger:
    def __init__(self):
        self._buffer = []
        self._flush_threshold = 100

    @lru_cache(maxsize=128)
    def _format_timestamp(self, ts):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ts))

    def log(self, message: str):
        entry = f"[{self._format_timestamp(time.time())}] {message}"
        self._buffer.append(entry)
        if len(self._buffer) >= self._flush_threshold:
            self.flush()

    def flush(self):
        if not self._buffer:
            return
        with open('crypto.log', 'a') as f:
            f.write('\n'.join(self._buffer) + '\n')
        self._buffer.clear()

# Singleton for shared performance state
stream_logger = AsyncLogger()