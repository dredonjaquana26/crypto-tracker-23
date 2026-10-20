[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# crypto-tracker-23

`crypto-tracker-23` is a lightweight Python library and terminal tool for tracking real-time cryptocurrency prices, portfolio performance, and market volatility. Built on top of the CoinGecko REST API, it delivers low-latency market updates with zero initial configuration required.

## Features

- **Real-Time Price Streams**: Monitor current prices, 24-hour volume, and market cap metrics for over 2,000 crypto assets.
- **Portfolio P&L Calculation**: Calculate live profit and loss balances against historical purchase points defined in a local JSON config.
- **Volatility Threshold Alerts**: Set automated console warnings when tracked assets drop or surge beyond custom percentage thresholds.
- **Data Export Utilities**: Export price snapshots and portfolio summaries directly to structured CSV and JSON formats.

## Installation

Ensure you have Python 3.9+ installed, then clone the repository and install the dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-23.git
cd crypto-tracker-23
pip install -r requirements.txt
```

## Quick Start

### Programmatic Usage

```python
from crypto_tracker import CryptoTracker

# Initialize the tracker for USD quotes
tracker = CryptoTracker(currency="usd")

# Fetch live metrics for targeted assets
data = tracker.get_prices(coins=["bitcoin", "ethereum", "solana"])

for coin, metrics in data.items():
    print(f"{coin.capitalize()}: ${metrics['price']:,.2f} | 24h: {metrics['change_24h']:+.2f}%")
```

### Command Line Interface

Run live monitoring directly from your terminal:

```bash
python -m crypto_tracker --coins bitcoin,ethereum --interval 15 --watch
```

## License

Distributed under the MIT License. See `LICENSE` for details.