import time
import random
from functools import wraps
from typing import Callable, Any, Tuple, Type

def fibonacci_jitter_retry(
    max_retries: int = 5,
    base_delay: float = 1.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,)
) -> Callable:
    """
    An unconventional decorator that uses a Fibonacci sequence generator
    with custom jitter to retry failing network operations.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            def fib_generator():
                a, b = base_delay, base_delay
                while True:
                    yield a
                    a, b = b, a + b
\            delay_gen = fib_generator()
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    last_exception = err
                    if attempt == max_retries:
                        break
                    
                    fib_wait = next(delay_gen)
                    jitter = random.uniform(0.1, 0.4) * fib_wait
                    sleep_time = fib_wait + jitter
                    
                    time.sleep(sleep_time)
            
            if last_exception:
                raise last_exception
        return wrapper
    return decorator