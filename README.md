# crypto-tracker-23

`crypto-tracker-23` is a lightweight Python command-line utility designed to monitor real-time cryptocurrency price fluctuations and historical trends. It leverages the CoinGecko API to provide accurate, up-to-the-second market data directly to your terminal.

## Features

*   **Live Price Streaming:** Fetch real-time market data for over 100+ top cryptocurrencies with configurable refresh intervals.
*   **Portfolio Tracking:** Monitor your personal holdings by defining a local CSV file, allowing the tool to calculate your total portfolio value in USD.
*   **Automated Alerts:** Set price thresholds for specific assets and receive desktop notifications when your targets are hit.
*   **Data Export:** Save snapshot market reports to JSON or CSV formats for integration with external analysis tools.

## Installation

Ensure you have Python 3.8+ installed. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-23.git
cd crypto-tracker-23
pip install -r requirements.txt
```

## Usage

To view the live dashboard for Bitcoin, Ethereum, and Solana, run the following command:

```bash
python tracker.py --assets btc,eth,sol --interval 60
```

To monitor your custom portfolio defined in `my_portfolio.csv`:

```bash
python tracker.py --portfolio my_portfolio.csv --alert-threshold 0.05
```

## Configuration

You can customize your experience by modifying the `config.ini` file located in the root directory. Update the `API_KEY` field if you are using a premium tier account, or adjust the default currency settings.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.