# Crypto-Tracker-23

Crypto-Tracker-23 is a lightweight Python command-line utility designed to monitor real-time cryptocurrency price movements and portfolio performance. It integrates directly with the CoinGecko API to provide accurate, up-to-the-second market data for traders and enthusiasts.

## Features

*   **Real-time Price Alerts:** Set custom threshold triggers to receive terminal notifications when a coin hits your target price.
*   **Portfolio Tracking:** Maintain a local JSON configuration to track total asset value and historical profit/loss performance.
*   **Data Visualization:** Generate ASCII-based trend charts directly in the terminal to visualize 24-hour price volatility.
*   **Multi-Currency Support:** Convert asset values into multiple fiat currencies including USD, EUR, and GBP.

## Installation

Ensure you have Python 3.8+ installed, then clone the repository and install the required dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-23.git
cd crypto-tracker-23
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Basic Usage

To monitor a specific set of assets defined in your `config.json`, run the main tracker script:

```bash
python main.py --monitor --symbols BTC,ETH,SOL
```

To fetch a snapshot of your current portfolio balance, use the following command:

```bash
python main.py --portfolio-value --currency USD
```

For a full list of available options and flags, run `python main.py --help`.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.