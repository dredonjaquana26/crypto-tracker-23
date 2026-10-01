import functools
import random
import time
from typing import Any, Callable, Sequence, Type, TypeVar

T = TypeVar("T")

def _fibonacci_jitter_stream(base: float = 0.5, max_delay: float = 20.0):
    a, b = base, base * 1.618
    while True:
        jitter = random.uniform(0.85, 1.15)
        yield min(a * jitter, max_delay)
        a, b = b, a + b

def retry_network_op(
    retries: int = 4,
    exceptions: Sequence[Type[BaseException]] = (Exception,),
    backoff_base: float = 0.5
):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delays = _fibonacci_jitter_stream(base=backoff_base)
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as err:
                    if attempt == retries:
                        raise err
                    sleep_time = next(delays)
                    time.sleep(sleep_time)
            raise RuntimeError("Unexpected end of retry sequence")
        return wrapper
    return decorator