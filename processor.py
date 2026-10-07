from typing import Iterable, Generator, Dict, Any

class TickStream:
    """Enables pipelined execution syntax using python's bitwise OR operator."""
    def __init__(self, data: Iterable[Dict[str, Any]]):
        self.data = data

    def __or__(self, processor: "StreamProcessor") -> "TickStream":
        return TickStream(processor.process(self.data))

    def collect(self) -> Generator[Dict[str, Any], None, None]:
        yield from self.data

class StreamProcessor:
    """Base representation of a stream processor filter."""
    def process(self, ticks: Iterable[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
        raise NotImplementedError

class VWAPCalculator(StreamProcessor):
    """Dynamic processor to calculate metrics like volume weighted average price on arbitrary batches."""
    def __init__(self, decimals: int = 4):
        self.decimals = decimals

    def process(self, ticks: Iterable[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
        accumulators: Dict[str, Dict[str, float]] = {}
        
        for tick in ticks:
            symbol = tick.get("symbol", "UNKNOWN")
            price = float(tick.get("price", 0.0))
            volume = float(tick.get("volume", 0.0))
            
            if symbol not in accumulators:
                accumulators[symbol] = {"sum_pv": 0.0, "sum_v": 0.0}
                
            accumulators[symbol]["sum_pv"] += price * volume
            accumulators[symbol]["sum_v"] += volume
            
        for symbol, metrics in accumulators.items():
            if metrics["sum_v"] > 0:
                vwap = metrics["sum_pv"] / metrics["sum_v"]
                yield {
                    "symbol": symbol,
                    "vwap": round(vwap, self.decimals),
                    "total_volume": round(metrics["sum_v"], self.decimals),
                }