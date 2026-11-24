import sys
import time
import collections
import functools

class AsyncOptimizedLogger:
    def __init__(self, capacity=1000):
        self.buffer = collections.deque(maxlen=capacity)
        self.last_flush = time.monotonic()

    def __call__(self, message: str):
        self.buffer.append(f"[{time.time()}] {message}")
        if len(self.buffer) >= self.buffer.maxlen:
            self.flush()

    def flush(self):
        if not self.buffer:
            return
        with open('crypto_ops.log', 'a') as f:
            f.write('\n'.join(self.buffer) + '\n')
        self.buffer.clear()
        self.last_flush = time.monotonic()

def batch_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        latency = (time.perf_counter() - start) * 1000
        if latency > 50:
            sys.stderr.write(f"[PERF WARNING] {func.__name__} took {latency:.2f}ms\n")
        return result
    return wrapper

log = AsyncOptimizedLogger()