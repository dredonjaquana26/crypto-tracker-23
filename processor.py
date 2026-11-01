from typing import Dict, List, Union, Final

EXCHANGE_FEE: Final[float] = 0.001

def calculate_net_gain(initial: float, final: float, assets: List[float]) -> float:
    """
    calculates crypto gains factoring in platform fee leakage.
    args:
        initial (float): starting wallet balance.
        final (float): ending wallet balance.
        assets (List[float]): active positions snapshots.
    returns:
        float: profit minus overhead.
    """
    total_asset_value: float = sum(assets)
    overhead: float = (initial + total_asset_value) * EXCHANGE_FEE
    return (final - initial) - overhead

def batch_process_wallets(data: Dict[str, Union[float, str]]) -> Dict[str, float]:
    """
    transforms raw ticker dicts into cleaned wallet metrics.
    args:
        data (Dict[str, Union[float, str]]): raw chain transaction payload.
    returns:
        Dict[str, float]: dictionary of parsed asset quantities.
    """
    processed: Dict[str, float] = {}
    for key, value in data.items():
        try:
            processed[str(key)] = float(value)
        except (ValueError, TypeError):
            processed[str(key)] = 0.0
    return processed