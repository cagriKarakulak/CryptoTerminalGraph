import ccxt
import time
import os
import shutil
import json
from datetime import datetime, timedelta
from art import text2art

exchange = ccxt.binance()

def fetch_btc_usdt_price(symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']  # Use the last price
    except ccxt.RequestTimeout:
        print("Request timed out. Retrying...")
        return None

def fetch_ohlcv_data(symbol, timeframe, limit):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        return ohlcv
    except ccxt.RequestTimeout:
        print("Request timed out. Retrying...")
        return None

def draw_realtime_graph(prices, timestamps, symbol):
    max_price = max(prices)
    min_price = min(prices)
    range_price = max_price - min_price

    # Get terminal size
    terminal_size = shutil.get_terminal_size((80, 20))
    graph_height = terminal_size.lines - 10  # Adjust for borders, labels, and title
    graph_width = max(int(terminal_size.columns * 0.7), 1)  # Use at least 70% of the terminal width
    border_width = terminal_size.columns - 2  # Full width for the border

    scaled_prices = [
        int((price - min_price) / range_price * (graph_height - 1)) if range_price > 0 else 0
    for price in prices]

    os.system('cls' if os.name == 'nt' else 'clear')
    print()  # Add an empty line for spacing
    title = text2art(f"{symbol} (Real-Time)")
    title_lines = title.split('\n')
    for line in title_lines:
        print(line.center(terminal_size.columns))  # Center the title text
    print("\033[1;37;40m+" + "-" * border_width + "+")  # Top border with color
    for i in range(graph_height):
        line = f"\033[1;37;40m{max_price - i * range_price / (graph_height - 1):.2f} |"  # Add price labels with color
        for j in range(graph_width):
            if j < len(scaled_prices) and graph_height - i - 1 == scaled_prices[j]:
                if j > 0:
                    if prices[j] > prices[j-1]:
                        line += '\033[1;32;40m█'  # Green block for upward price points
                    elif prices[j] < prices[j-1]:
                        line += '\033[1;31;40m█'  # Red block for downward price points
                    else:
                        line += line[-1]  # Retain previous color if price is unchanged
                else:
                    line += '\033[1;32;40m█'  # Default to green for the first point
            elif j > 0 and j < len(scaled_prices):
                if scaled_prices[j] > scaled_prices[j-1]:
                    line_color = '\033[1;32;40m|'  # Green color for upward lines
                else:
                    line_color = '\033[1;31;40m|'  # Red color for downward lines
                if graph_height - i - 1 in range(min(scaled_prices[j-1], scaled_prices[j]), max(scaled_prices[j-1], scaled_prices[j]) + 1):
                    line += line_color
                else:
                    line += ' '
            else:
                line += ' '
        line += "\033[1;37;40m" + " " * (border_width - graph_width - 8) + "|"  # Fill the rest of the line with spaces and border
        print(line)
    print("+" + "-" * border_width + "+\033[0m")  # Bottom border with color

def draw_candlestick_graph(ohlcv_data, symbol, timeframe, time_remaining):
    max_price = max([candle[2] for candle in ohlcv_data])  # High prices
    min_price = min([candle[3] for candle in ohlcv_data])  # Low prices
    range_price = max_price - min_price

    # Get terminal size
    terminal_size = shutil.get_terminal_size((80, 20))
    graph_height = terminal_size.lines - 12  # Adjust for borders, labels, title, and time remaining
    graph_width = max(int(terminal_size.columns * 0.7), 1)  # Use at least 70% of the terminal width
    border_width = terminal_size.columns - 2  # Full width for the border

    scaled_highs = [
        int((candle[2] - min_price) / range_price * (graph_height - 1)) if range_price > 0 else 0
    for candle in ohlcv_data]

    scaled_lows = [
        int((candle[3] - min_price) / range_price * (graph_height - 1)) if range_price > 0 else 0
    for candle in ohlcv_data]

    os.system('cls' if os.name == 'nt' else 'clear')
    print()  # Add an empty line for spacing
    title = text2art(f"{symbol} ({timeframe})")
    title_lines = title.split('\n')
    for line in title_lines:
        print(line.center(terminal_size.columns))  # Center the title text
    print("\033[1;37;40m+" + "-" * border_width + "+")  # Top border with color
    for i in range(graph_height):
        line = f"\033[1;37;40m{max_price - i * range_price / (graph_height - 1):.2f} |"  # Add price labels with color
        for j in range(graph_width):
            if j < len(scaled_highs) and j < len(scaled_lows) and graph_height - i - 1 <= scaled_highs[j] and graph_height - i - 1 >= scaled_lows[j]:
                if ohlcv_data[j][1] < ohlcv_data[j][4]:  # Green candlestick
                    if graph_height - i - 1 == scaled_highs[j] or graph_height - i - 1 == scaled_lows[j]:
                        line += '\033[1;32;40m|'  # Green wick
                    else:
                        line += '\033[1;32;40m█'  # Green body
                else:  # Red candlestick
                    if graph_height - i - 1 == scaled_highs[j] or graph_height - i - 1 == scaled_lows[j]:
                        line += '\033[1;31;40m|'  # Red wick
                    else:
                        line += '\033[1;31;40m█'  # Red body
            else:
                line += ' '
        line += "\033[1;37;40m" + " " * (border_width - graph_width - 8) + "|"  # Fill the rest of the line with spaces and border
        print(line)
    print("+" + "-" * border_width + "+\033[0m")  # Bottom border with color

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    symbol = config['symbol']
    mode = config['mode']
    timeframe = config.get('timeframe', '1m')

    prices = []
    timestamps = []
    while True:
        donguBaslangici = time.time()
        with open('config.json', 'r') as f:
            config = json.load(f)
        symbol = config['symbol']
        mode = config['mode']
        timeframe = config.get('timeframe', '1m')
        terminal_size = shutil.get_terminal_size((80, 20))
        limit = max(int(terminal_size.columns * 0.7), 1)  # Adjust limit based on terminal width, at least 1
        if mode == 'realtime':
            price = fetch_btc_usdt_price(symbol)
            if price is not None:
                prices.append(price)
                timestamps.append(datetime.now())
                if len(prices) > 1000:  # Keep a large number of prices in memory
                    prices.pop(0)
                    timestamps.pop(0)
                draw_realtime_graph(prices[-limit:], timestamps[-limit:], symbol)
        elif mode == 'ohlcv':
            ohlcv_data = fetch_ohlcv_data(symbol, timeframe, limit)
            if ohlcv_data is not None:
                current_time = datetime.now()
                next_candle_time = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
                time_remaining = (next_candle_time - current_time).seconds
                draw_candlestick_graph(ohlcv_data, symbol, timeframe, time_remaining)
        print(f"Time remaining: {time_remaining} seconds")
        print("Delay:", round(time.time() - donguBaslangici, 2), "seconds")

if __name__ == "__main__":
    print("Starting the program...")  # Debug print
    main()
