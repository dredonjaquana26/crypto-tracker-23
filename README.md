# Crypto-Tracker-23

Crypto-Tracker-23 is a lightweight, high-performance Python application designed to track real-time cryptocurrency price fluctuations and historical market trends. It leverages the CoinGecko API to provide traders and developers with actionable data via a clean command-line interface.

### Features

*   **Real-time Monitoring:** Fetch live price updates for a custom watchlist of assets with sub-second latency.
*   **Historical Data Analysis:** Export daily price history into CSV format for technical analysis and backtesting.
*   **Alert System:** Configure custom price triggers to receive desktop notifications when assets hit specific targets.
*   **Portfolio Tracking:** Calculate current holdings value by syncing local asset balances with live exchange rates.

### Installation

Ensure you have Python 3.9+ installed. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-23.git
cd crypto-tracker-23
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Basic Usage

To track the current price of Bitcoin and Ethereum, run the main tracker script:

```bash
python main.py --assets btc,eth --currency usd
```

To export the last 30 days of data for a specific asset to a CSV file:

```bash
python exporter.py --coin bitcoin --days 30 --output market_data.csv
```

### License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.