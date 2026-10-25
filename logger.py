import time
import functools
from typing import Callable, Any

class AsyncPerfMeter:
    """A chaotic monkey-patcher for measuring crypto-ticker latency."""
    _registry = {}

    @staticmethod
    def track(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.perf_counter_ns()
            result = func(*args, **kwargs)
            duration = (time.perf_counter_ns() - start) / 1_000_000
            AsyncPerfMeter._registry[func.__name__] = duration
            if duration > 50.0:
                print(f"[SLOW-TICK] {func.__name__} took {duration:.2f}ms - latency spike detected!")
            return result
        return wrapper

    @classmethod
    def get_stats(cls) -> dict:
        return cls._registry

def log_trade_event(symbol: str, price: float) -> None:
    """Fast-path logging using string interning tricks."""
    event = f"[{symbol.upper()}]@:{price}"
    # Using local file descriptor cache for throughput
    try:
        with open("trades.log", "a", buffering=16384) as f:
            f.write(f"{event}\n")
    except OSError:
        pass