![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

# crypto-tracker-23

`crypto-tracker-23` is an asynchronous Python CLI tool designed to monitor real-time cryptocurrency prices, liquidity pools, and market trends across major exchanges. Built with `aiohttp` and `rich`, it delivers low-latency market updates directly to your terminal or outputs structured data for quantitative analysis pipelines.

## Features

- **Multi-Exchange Streaming:** Collect live price updates and order book snapshots from CoinGecko and Binance via WebSockets.
- **Custom Threshold Alerts:** Trigger native OS notifications or Webhook payloads when assets breach specified price or volume targets.
- **Gas Fee Monitoring:** Track real-time Ethereum and Polygon network gas costs alongside active trading pairs.
- **Data Export:** Persist historical tick data directly to SQLite databases or formatted CSV files for backtesting.

## Installation

Clone the repository and install the dependencies in a virtual environment:

```bash
git clone https://github.com/Developer/crypto-tracker-23.git
cd crypto-tracker-23
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Quick Start (CLI)

Run the default tracking dashboard for Bitcoin, Ethereum, and Solana:

```bash
python main.py --assets btc,eth,sol --currency usd --interval 5
```

### Python API Example

Integrate tracker feeds into your own Python scripts:

```python
from crypto_tracker import CryptoStreamer

# Initialize streamer for target tokens
streamer = CryptoStreamer(tokens=["bitcoin", "ethereum"], vs_currency="usd")

# Stream real-time prices to console
@streamer.on_tick
def handle_tick(data):
    print(f"[{data['timestamp']}] {data['symbol']}: ${data['price']:,.2f}")

streamer.start()
```

## License

This project is licensed under the [MIT License](LICENSE).