import functools
import logging
import random
import time
from typing import Any, Callable, Tuple, Type

logger = logging.getLogger("crypto_tracker.network")


def _fibonacci_generator():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


def network_retry(
    max_attempts: int = 5,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    use_fibonacci: bool = True,
) -> Callable:
    """Retry decorator with fibonacci backoff and golden-ratio jitter for crypto APIs."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            fib = _fibonacci_generator()
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt == max_attempts:
                        logger.error("Max retries reached for %s: %s", func.__name__, err)
                        raise

                    base_delay = next(fib) if use_fibonacci else (2 ** attempt)
                    # Golden ratio (1.618) micro-jitter to prevent synchronized ticker polling
                    jitter = random.uniform(0.1, 1.618)
                    delay = base_delay + jitter

                    logger.warning(
                        "Attempt %d/%d failed for %s (%s). Retrying in %.2fs...",
                        attempt, max_attempts, func.__name__, err, delay
                    )
                    time.sleep(delay)
        return wrapper
    return decorator
