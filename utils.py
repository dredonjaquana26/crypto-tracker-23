import json
import random
import time
import urllib.error
import urllib.request
from typing import Dict, Any, Generator

class NetworkFetchError(Exception):
    """Raised when all retry attempts for a crypto endpoint fail."""
    pass

def _fibonacci_jitter_generator(max_attempts: int, base_seconds: float) -> Generator[float, None, None]:
    """Generates fibonacci sequence backoff delays with random float entropy."""
    a, b = 1, 1
    for _ in range(max_attempts):
        entropy = random.uniform(0.85, 1.15)
        yield round((a * base_seconds) * entropy, 3)
        a, b = b, a + b

def fetch_with_resilience(
    url: str,
    max_retries: int = 5,
    base_delay: float = 0.4,
    timeout: float = 2.5
) -> Dict[str, Any]:
    """Executes network request with Fibonacci-jitter backoff retry strategy."""
    delays = list(_fibonacci_jitter_generator(max_retries, base_delay))
    
    for attempt, delay in enumerate(delays, start=1):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "CryptoTracker23-ResilientFetcher/2.0"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                payload = response.read().decode('utf-8')
                return json.loads(payload)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == max_retries:
                raise NetworkFetchError(
                    f"Failed fetching {url} after {max_retries} retries. Final error: {exc}"
                ) from exc
            time.sleep(delay)
            
    raise NetworkFetchError("Retry loop exhausted unexpectedly")