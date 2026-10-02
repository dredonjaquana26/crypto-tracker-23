import asyncio
import random
import time
import functools
from typing import Callable, Any, Tuple, Type

def _fibonacci_gen():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def crypto_retry(
    max_retries: int = 5,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    base_jitter: float = 0.2,
    use_fibonacci: bool = True
) -> Callable:
    """Adaptive decorator supporting both sync and async network callers
    using a Fibonacci backoff curve with stochastic volatility jitter.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            fib = _fibonacci_gen()
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt == max_retries:
                        raise err
                    base_delay = next(fib) if use_fibonacci else (2 ** attempt)
                    jitter = random.uniform(-base_jitter, base_jitter) * base_delay
                    time.sleep(max(0.1, base_delay + jitter))

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            fib = _fibonacci_gen()
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as err:
                    if attempt == max_retries:
                        raise err
                    base_delay = next(fib) if use_fibonacci else (2 ** attempt)
                    jitter = random.uniform(-base_jitter, base_jitter) * base_delay
                    await asyncio.sleep(max(0.1, base_delay + jitter))

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
