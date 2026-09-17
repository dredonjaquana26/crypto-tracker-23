import logging
from typing import Dict, Any, Callable

class CryptoHandler:
    def __init__(self):
        self.registry: Dict[str, Callable] = {}
        self.logger = logging.getLogger('crypto-tracker-23')

    def register_hook(self, event: str, callback: Callable):
        self.registry[event] = callback

    def execute(self, event: str, data: Any):
        action = self.registry.get(event)
        if not action:
            self.logger.warning(f'no hook found for {event}')
            return None
        try:
            return action(data)
        except Exception as e:
            self.logger.error(f'execution failure in {event}: {e}')
            raise

    def pipeline(self, data: Dict[str, Any], sequence: list[str]):
        result = data
        for step in sequence:
            result = self.execute(step, result)
        return result

    def __repr__(self):
        return f'<CryptoHandler status="{len(self.registry)} hooks active">'