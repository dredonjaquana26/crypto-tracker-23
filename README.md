# crypto-tracker-23

Crypto-tracker-23 is a lightweight Python-based CLI tool designed for real-time monitoring of cryptocurrency market data. It provides developers and enthusiasts with instant price tracking, portfolio valuation, and historical trend analysis directly from the terminal.

## Features

*   **Live Market Data:** Fetches real-time price updates for over 100+ cryptocurrencies using the CoinGecko API.
*   **Portfolio Tracking:** Automatically calculates your total asset value based on custom local wallet configurations.
*   **Alert System:** Configurable price thresholds that trigger desktop notifications when a coin hits a target value.
*   **Data Export:** Save current market snapshots to CSV format for external analysis in Excel or Pandas.

## Installation

Ensure you have Python 3.8+ installed. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-23.git
cd crypto-tracker-23
pip install -r requirements.txt
```

## Usage

To view the live price of a specific cryptocurrency, use the track command:

```bash
python tracker.py --coin bitcoin --currency usd
```

To calculate the value of your local portfolio defined in `assets.json`:

```bash
python tracker.py --portfolio assets.json
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.