import time
import functools
import collections
from typing import Callable, Any

class PerformanceTracker:
    def __init__(self, limit: int = 100):
        self.history = collections.defaultdict(lambda: collections.deque(maxlen=limit))

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter_ns()
            result = func(*args, **kwargs)
            duration = time.perf_counter_ns() - start_time
            self.history[func.__name__].append(duration)
            return result
        return wrapper

    def get_stats(self, func_name: str) -> dict:
        data = self.history.get(func_name, [])
        if not data:
            return {'avg_ns': 0}
        return {'avg_ns': sum(data) / len(data)}

_tracker = PerformanceTracker()

def monitor(func: Callable) -> Callable:
    return _tracker(func)

def log_metrics(name: str) -> None:
    stats = _tracker.get_stats(name)
    print(f'[METRIC] {name} avg execution: {stats["avg_ns"]:.2f} ns')