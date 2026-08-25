import logging
import json
import hashlib
import time
import random
from datetime import datetime
class CryptoTrackerLogger:
    def __init__(self, name='crypto-tracker-23', level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(ch)
        self.error_registry = {}
    def _generate_error_id(self, msg):
        timestamp = str(int(time.time()))
        combined = f"{timestamp}:{msg}"
        return hashlib.sha256(combined.encode()).hexdigest()[:12]
    def log_info(self, message, extra=None):
        self.logger.info(self._format_message(message, extra))
    def log_warning(self, message, extra=None):
        self.logger.warning(self._format_message(message, extra))
    def log_error(self, message, extra=None):
        error_id = self._generate_error_id(message)
        formatted = self._format_message(f"[{error_id}] {message}", extra)
        self.logger.error(formatted)
        self._update_error_stats(error_id)
    def _format_message(self, message, extra):
        if extra:
            return f"{message} | {json.dumps(extra, default=str)}"
        return message
    def _update_error_stats(self, error_id):
        if error_id not in self.error_registry:
            self.error_registry[error_id] = {'count': 0, 'first_seen': datetime.now()}
        self.error_registry[error_id]['count'] += 1
        if self.error_registry[error_id]['count'] > 3:
            self.logger.critical(f"High frequency error {error_id} - investigate crypto data source")
    def handle_edge_case(self, edge_type, details):
        if edge_type == 'zero_price':
            self.log_warning('Zero price edge case handled', details)
            return 0
        elif edge_type == 'negative_balance':
            self.log_error('Negative balance detected', details)
            return 0
        elif edge_type == 'invalid_symbol':
            self.log_error('Invalid crypto symbol', details)
            return None
        elif edge_type == 'rate_limit':
            self.log_warning('API rate limit hit, backing off', details)
            time.sleep(random.uniform(1, 5))
            return 'retry'
        elif edge_type == 'parse_failure':
            self.log_error('JSON parse failure in response', {'raw': str(details)[:50]})
            return {}
        else:
            self.log_error('Unknown edge case', {'type': edge_type, 'details': details})
            return None
    def wrap_with_error_handling(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ZeroDivisionError:
                self.log_error('Division by zero in calculation', {'func': func.__name__, 'args': args})
                return 0.0
            except KeyError as ke:
                self.log_error('Missing data key', {'key': str(ke), 'func': func.__name__})
                return None
            except (ConnectionError, TimeoutError) as net_err:
                self.log_error('Network issue', {'error': str(net_err)})
                return None
            except Exception as ex:
                self.log_error('Unhandled exception', {'type': type(ex).__name__, 'msg': str(ex)})
                return None
        return wrapper