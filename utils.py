import time
import functools
import logging

logger = logging.getLogger('crypto-tracker-23')

def resilient_network_call(max_retries=3, backoff_factor=1.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = 1.0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_retries:
                        logger.error(f'Exhausted retries for {func.__name__}: {e}')
                        raise
                    logger.warning(f'Attempt {attempts} failed, sleeping {delay}s...')
                    time.sleep(delay)
                    delay *= backoff_factor
        return wrapper
    return decorator

def async_retry_shield(func):
    async def async_wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return await func(*args, **kwargs)
            except Exception:
                if i == 2: raise
                await __import__('asyncio').sleep(2 ** i)
    return async_wrapper