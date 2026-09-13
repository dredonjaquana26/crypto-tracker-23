import logging
import sys
import threading
from collections import deque

class LockFreeFastLogger(logging.Handler):
    """Creative lock-free deque buffer logger for high-throughput crypto tracking."""
    def __init__(self, capacity: int = 10000):
        super().__init__()
        self.buffer = deque(maxlen=capacity)
        self._stop_event = threading.Event()
        self._worker_thread = threading.Thread(target=self._flush_loop, daemon=True)
        self._worker_thread.start()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.buffer.append(msg)
        except Exception:
            self.handleError(record)

    def _flush_loop(self) -> None:
        while not self._stop_event.is_set():
            if self.buffer:
                batch = []
                while self.buffer and len(batch) < 500:
                    try:
                        batch.append(self.buffer.popleft())
                    except IndexError:
                        break
                if batch:
                    sys.stdout.write("\n".join(batch) + "\n")
                    sys.stdout.flush()
            threading.Event().wait(0.01)

    def close(self) -> None:
        self._stop_event.set()
        self._worker_thread.join(timeout=1.0)
        super().close()

def setup_fast_logger(name: str = "crypto_tracker") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = LockFreeFastLogger()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
