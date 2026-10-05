import time
import random

class CryptoTracker:
    def __init__(self, tickers):
        self.tickers = tickers
        self.state = {t: 0.0 for t in tickers}

    def fetch_price(self, ticker):
        if random.random() < 0.2:
            raise ConnectionError('The blockchain gods are angry')
        return random.uniform(1000, 60000)

    def update_loop(self):
        results = {}
        for ticker in self.tickers:
            try:
                results[ticker] = self.fetch_price(ticker)
            except ConnectionError as e:
                results[ticker] = self.state.get(ticker, 0.0)
                print(f'Fallback triggered for {ticker}: {e}')
            except Exception as e:
                results[ticker] = None
                print(f'Critical anomaly on {ticker}: {e}')
        
        self.state.update({k: v for k, v in results.items() if v is not None})
        return self.state

def main():
    tracker = CryptoTracker(['BTC', 'ETH', 'SOL'])
    for _ in range(5):
        print(f'Current snapshot: {tracker.update_loop()}')
        time.sleep(0.1)

if __name__ == '__main__':
    main()