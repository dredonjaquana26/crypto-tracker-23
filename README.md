# crypto-tracker-23

A high-performance Python CLI tool designed to track real-time cryptocurrency market data and portfolio performance. It leverages the CoinGecko API to provide accurate price feeds and historical trend analysis directly in your terminal.

## Features

*   **Live Price Monitoring:** Fetches sub-second price updates for top 100 cryptocurrencies with customizable refresh intervals.
*   **Portfolio Tracking:** Automatically calculates total holdings value by ingesting a local `assets.json` configuration file.
*   **Historical Analysis:** Generates ASCII-based trend charts to visualize price volatility over the last 24 hours.
*   **Alert System:** Configurable threshold notifications that trigger desktop alerts when a coin hits a specified buy or sell price.

## Installation

Ensure you have Python 3.8+ installed. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-23.git
cd crypto-tracker-23
pip install -r requirements.txt
```

## Usage

To view the current market dashboard, run the main entry point:

```bash
python main.py --view market
```

To track your custom portfolio defined in `assets.json`:

```bash
python main.py --track portfolio --file assets.json
```

For a full list of commands and available exchange markets, use the help flag:

```bash
python main.py --help
```

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.