# crypto-tracker-23

Crypto-tracker-23 is a lightweight Python command-line utility that provides real-time monitoring and historical price tracking for major cryptocurrencies. It leverages the CoinGecko API to deliver accurate market data and customizable price alerts directly to your terminal.

### Key Features
*   **Live Price Monitoring:** Fetches sub-second market data for top-performing assets using an optimized asynchronous API client.
*   **Portfolio Snapshot:** Calculates total portfolio value in USD based on user-defined holdings and live market rates.
*   **Threshold Alerts:** Set custom trigger prices and receive desktop notifications when an asset hits your target buy or sell range.
*   **Data Persistence:** Saves session history into local CSV files for quick trend analysis and auditing.

### Installation

Ensure you have Python 3.8+ installed. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Developer/crypto-tracker-23.git
cd crypto-tracker-23
pip install -r requirements.txt
```

### Usage

To start the tracker and view live prices for your watch-list, run the main entry point:

```bash
python main.py --watch BTC,ETH,SOL
```

To configure portfolio holdings and enable automated price alerts, modify the `config.yaml` file and execute:

```bash
python main.py --monitor --interval 60
```

This will run the tracker in a persistent loop, checking prices every 60 seconds and alerting you if defined thresholds are crossed.

### License
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.