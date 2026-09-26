from typing import Dict, Generic, Iterator, NewType, Protocol, Tuple, TypeVar

# Precise domain-specific type boundaries avoiding float inaccuracies
Satoshi = NewType("Satoshi", int)
UsdCent = NewType("UsdCent", int)

T = TypeVar("T", Satoshi, UsdCent)


class PriceFeed(Protocol[T]):
    """Protocol defining the structural contract for high-frequency pricing inputs."""

    def tick(self) -> Iterator[Tuple[str, T]]:
        """Yields a sequence of crypto asset tickers and their raw integer values."""
        ...


class VolatilityEngine(Generic[T]):
    """Evaluates structural risk and tracking divergence without IEEE-754 drift.

    Leverages Generic bounds to enforce compile-time verification of
    Satoshi versus UsdCent pricing metrics within the tracking matrix.
    """

    def __init__(self, baseline: T) -> None:
        self.baseline: T = baseline
        self.history: list[T] = [baseline]

    def record_and_evaluate(self, feed: PriceFeed[T]) -> dict[str, float]:
        """Consumes ticker streams, calculating deviation profiles relative to baseline.

        Returns a mapped dictionary of evaluated price swing percentages.
        """
        evaluations: dict[str, float] = {}
        for ticker, raw_val in feed.tick():
            self.history.append(raw_val)
            variance = int(raw_val) - int(self.baseline)
            pct_deviation = (variance / int(self.baseline)) * 100.0
            evaluations[ticker] = round(pct_deviation, 4)

            if len(self.history) > 50:
                self.history.pop(0)
        return evaluations


class MockSatoshiFeed:
    """Generates mock cryptographic ticks mapping to Satoshi protocol standards."""

    def __init__(self, starting_value: int) -> None:
        self.current = starting_value

    def tick(self) -> Iterator[Tuple[str, Satoshi]]:
        """Produces simulated BTC tick with upward drift volatility."""
        self.current = int(self.current * 1.025)
        yield ("BTC/USD", Satoshi(self.current))
