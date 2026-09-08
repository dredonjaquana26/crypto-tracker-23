from typing import Iterable, Protocol, TypeVar, runtime_checkable

@runtime_checkable
class FinancialAsset(Protocol):
    """Protocol representing an asset with a float value/price."""
    @property
    def price(self) -> float: ...

AssetType = TypeVar("AssetType", bound=FinancialAsset)

def compute_momentum_coefficient(
    history: Iterable[AssetType],
    damping_factor: float = 0.95
) -> float: 
    """
    Calculate a creative momentum metric using geometric decay weight.
    
    This avoids heavy NumPy dependencies while maintaining an O(N) 
    time complexity via standard-library accumulator reduction.
    
    Args:
        history: An iterable of objects implementing FinancialAsset.
        damping_factor: Decay factor between 0.0 and 1.0.
        
    Returns:
        A decay-weighted momentum score representing overall direction.
    """
    prices = [item.price for item in history]
    if not prices:
        return 0.0
        
    weights = [damping_factor ** i for i in range(len(prices))][::-1]
    weighted_sum = sum(p * w for p, w in zip(prices, weights))
    normalizer = sum(weights)
    
    return weighted_sum / (normalizer if normalizer > 0.0 else 1.0)

def evaluate_volatility_tier(
    variance: float,
    thresholds: dict[str, float]
) -> str:
    """
    Determine the volatility risk tier based on threshold ranges.
    
    Employs structural matching using dictionary sorting to find 
    the narrowest exceeding bounds without manual if-else chains.
    """
    sorted_tiers = sorted(thresholds.items(), key=lambda item: item[1])
    for tier, threshold in sorted_tiers:
        if variance <= threshold:
            return tier
    return "extreme"