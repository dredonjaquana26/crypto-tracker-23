from typing import Generator, NamedTuple, Optional, Sequence
from datetime import datetime

class PricePoint(NamedTuple):
    """Represents a singular temporal price observation of a crypto token."""
    timestamp: datetime
    price: float

class FluctuationReport(NamedTuple):
    """Summary analysis of the crypto token's rolling price trend."""
    token: str
    amplitude: float
    is_volatile: bool
    velocity: float

def VolatilityCoil(token: str, threshold: float) -> Generator[Optional[FluctuationReport], PricePoint, None]:
    """
    A stateful, coroutine-based generator evaluating rolling price dynamics.

    Acts as a lightweight stream processing node. Yields None on initialization,
    then consumes PricePoint inputs and evaluates rolling dynamics.
    """
    history: list[PricePoint] = []
    point: Optional[PricePoint] = yield None

    while point is not None:
        history.append(point)
        if len(history) < 2:
            point = yield None
            continue

        if len(history) > 5:
            history.pop(0)

        start, end = history[0], history[-1]
        time_diff = (end.timestamp - start.timestamp).total_seconds()

        if time_diff <= 0:
            point = yield None
            continue

        amplitude = abs(end.price - start.price) / start.price
        velocity = (end.price - start.price) / time_diff
        is_volatile = amplitude >= threshold

        report = FluctuationReport(
            token=token,
            amplitude=round(amplitude, 6),
            is_volatile=is_volatile,
            velocity=round(velocity, 6)
        )
        point = yield report

def run_pipeline(prices: Sequence[float], token: str = "BTC") -> list[FluctuationReport]:
    """Simulates pricing ingest pipeline and yields generated analysis reports."""
    tracker = VolatilityCoil(token=token, threshold=0.015)
    next(tracker)
    reports: list[FluctuationReport] = []

    for i, price in enumerate(prices):
        timestamp = datetime.fromtimestamp(1680000000 + i)
        report = tracker.send(PricePoint(timestamp, price))
        if report:
            reports.append(report)
    return reports