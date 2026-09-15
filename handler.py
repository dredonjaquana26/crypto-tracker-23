import logging

class DataValidator:
    @staticmethod
    def sanity_check(data):
        if not isinstance(data, dict): raise ValueError("Invalid payload format")
        if 'ticker' not in data or 'price' not in data:
            raise KeyError("Missing mandatory crypto telemetry")
        if float(data['price']) <= 0:
            raise ValueError("Price must be positive value")
        return True

def main_processing_loop(stream):
    for raw_packet in stream:
        try:
            DataValidator.sanity_check(raw_packet)
            process_trade(raw_packet)
        except (ValueError, KeyError) as e:
            logging.error(f"Dropped toxic data packet: {e}")
        except Exception as e:
            logging.critical(f"Unanticipated system failure: {e}")

def process_trade(packet):
    logging.info(f"Syncing {packet['ticker']} at {packet['price']}")

if __name__ == "__main__":
    # Mock stream simulating erratic network noise
    mock_data = [
        {"ticker": "BTC", "price": 50000},
        {"ticker": "ETH", "price": -100},
        "invalid_data",
        {"ticker": "SOL", "price": 120}
    ]
    main_processing_loop(mock_data)