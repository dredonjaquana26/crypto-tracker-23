# Crypto Tracker 23

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

Crypto Tracker 23 is a lightweight, high-performance command-line interface tool designed for real-time cryptocurrency portfolio monitoring and market analysis. It connects directly to public exchange APIs to deliver low-latency price feeds and automated profit-and-loss calculations straight to your terminal.

## Features

- **Live Price Streaming:** Fetches second-by-second ticker data and order book depth for major trading pairs using asynchronous HTTP requests.
- **Automated Portfolio Valuation:** Calculates total portfolio value, daily gains/losses, and asset allocation percentages based on local CSV transaction logs.
- **Custom Price Alerts:** Triggers desktop notifications or terminal sound alerts when specified threshold prices are breached.
- **Historical CSV Export:** Dumps raw OHLCV (Open, High, Low, Close, Volume) data into structured CSV files for backtesting and technical analysis.

## Installation

Ensure you have Python 3.10 or higher installed on your system. 

```bash
# Clone the repository
git clone https://github.com/Developer/crypto-tracker-23.git
cd crypto-tracker-23

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Configure your portfolio holdings in `config/portfolio.json`, then launch the tracker from your terminal.

```bash
# Run the application with default settings
python main.py --config config/portfolio.json

# Stream live prices for specific assets only
python main.py --symbols BTC,ETH,SOL --interval 5
```

To run a quick one-time market summary without loading a portfolio file:

```bash
python main.py --market-only --top 10
```

## Project Structure

```text
crypto-tracker-23/
├── config/          # User portfolio and alert configurations
├── src/             # Core API connectors and calculation engines
├── data/            # Exported historical CSV datasets
├── main.py          # Entry point for the CLI application
└── requirements.txt # Project dependencies
```

## License

Distributed under the MIT License. See `LICENSE` for more information.