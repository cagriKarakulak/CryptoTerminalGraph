# CryptoTerminalGraph
![Untitled](https://github.com/user-attachments/assets/6a551850-351f-4b2b-b77f-dd1395379e66)

This project fetches and displays real-time and OHLCV (Open, High, Low, Close, Volume) data for a specified cryptocurrency pair using the Binance exchange. The data is visualized in the terminal as either a real-time price graph or a candlestick chart, depending on the configuration.

## Features

- **Real-Time Price Graph**: Displays the latest price data in real-time.
- **OHLCV Candlestick Chart**: Displays historical candlestick data for various timeframes.
- **Dynamic Terminal Size**: Adjusts the graph size based on the terminal window size.
- **Configurable Settings**: Allows customization of the cryptocurrency pair, mode (real-time or OHLCV), and timeframe through a JSON configuration file.

## Requirements

- Python 3.x
- `ccxt` library
- `art` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/cagriKarakulak/CryptoTerminalGraph.git
    cd CryptoTerminalGraph
    ```

2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

The configuration is managed through the `config.json` file. Here is an example configuration:

```json
{
    "symbol": "BTC/USDT",
    "mode": "ohlcv",  // Change to "realtime" for real-time price graph
    "timeframe": "1m" // Only used if mode is "ohlcv"
}
```

- `symbol`: The cryptocurrency pair to fetch data for.
- `mode`: The mode of the graph. Can be `realtime` for real-time price graph or `ohlcv` for candlestick chart.
- `timeframe`: The timeframe for OHLCV data. Only used if mode is `ohlcv`.

## Usage

Run the main script to start the program:

```sh
python chart.py
```

The program will read the configuration from `config.json` and display the graph accordingly.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
