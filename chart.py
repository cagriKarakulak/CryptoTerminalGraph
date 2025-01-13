import ccxt
import time
import os
import shutil
import json
from datetime import datetime, timedelta
from art import text2art

exchange = ccxt.binance()

def fetch_price(symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
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

def draw_realtime_graph(prices, symbol):
    max_price = max(prices)
    min_price = min(prices)
    range_price = max_price - min_price

    terminal_size = shutil.get_terminal_size((80, 20))
    graph_height = terminal_size.lines - 10
    graph_width = max(int(terminal_size.columns * 0.7), 1)
    border_width = terminal_size.columns - 2

    scaled_prices = [
        int((price - min_price) / range_price * (graph_height - 1)) if range_price > 0 else 0
    for price in prices]

    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    title = text2art(f"{symbol} (Real-Time)")
    title_lines = title.split('\n')
    for line in title_lines:
        print(line.center(terminal_size.columns))
    print("\033[1;37;40m+" + "-" * border_width + "+")
    for i in range(graph_height):
        line = f"\033[1;37;40m{max_price - i * range_price / (graph_height - 1):.2f} |"
        for j in range(graph_width):
            if j < len(scaled_prices) and graph_height - i - 1 == scaled_prices[j]:
                if j > 0:
                    if prices[j] > prices[j-1]:
                        line += '\033[1;32;40m█'
                    elif prices[j] < prices[j-1]:
                        line += '\033[1;31;40m█'
                    else:
                        line += line[-1]
                else:
                    line += '\033[1;32;40m█'
            elif j > 0 and j < len(scaled_prices):
                if scaled_prices[j] > scaled_prices[j-1]:
                    line_color = '\033[1;32;40m|'
                else:
                    line_color = '\033[1;31;40m|'
                if graph_height - i - 1 in range(min(scaled_prices[j-1], scaled_prices[j]), max(scaled_prices[j-1], scaled_prices[j]) + 1):
                    line += line_color
                else:
                    line += ' '
            else:
                line += ' '
        line += "\033[1;37;40m" + " " * (border_width - graph_width - 8) + "|"
        print(line)
    print("+" + "-" * border_width + "+\033[0m")

def draw_candlestick_graph(ohlcv_data, symbol, timeframe):
    max_price = max([candle[2] for candle in ohlcv_data])
    min_price = min([candle[3] for candle in ohlcv_data])
    range_price = max_price - min_price

    terminal_size = shutil.get_terminal_size((80, 20))
    graph_height = terminal_size.lines - 12
    graph_width = max(int(terminal_size.columns * 0.7), 1)
    border_width = terminal_size.columns - 2

    scaled_highs = [
        int((candle[2] - min_price) / range_price * (graph_height - 1)) if range_price > 0 else 0
    for candle in ohlcv_data]

    scaled_lows = [
        int((candle[3] - min_price) / range_price * (graph_height - 1)) if range_price > 0 else 0
    for candle in ohlcv_data]

    scaled_opens = [
        int((candle[1] - min_price) / range_price * (graph_height - 1)) if range_price > 0 else 0
    for candle in ohlcv_data]

    scaled_closes = [
        int((candle[4] - min_price) / range_price * (graph_height - 1)) if range_price > 0 else 0
    for candle in ohlcv_data]

    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    title = text2art(f"{symbol} ({timeframe})")
    title_lines = title.split('\n')
    for line in title_lines:
        print(line.center(terminal_size.columns))
    print("\033[1;37;40m+" + "-" * border_width + "+")
    previous_color = '\033[1;32;40m' 
    for i in range(graph_height):
        line = f"\033[1;37;40m{max_price - i * range_price / (graph_height - 1):.2f} |"
        for j in range(graph_width):
            if j < len(scaled_highs) and j < len(scaled_lows):
                if graph_height - i - 1 <= scaled_highs[j] and graph_height - i - 1 >= scaled_lows[j]:
                    if scaled_opens[j] < scaled_closes[j]:
                        color = '\033[1;32;40m'
                    elif scaled_opens[j] > scaled_closes[j]:
                        color = '\033[1;31;40m'
                    else:
                        color = previous_color

                    if graph_height - i - 1 <= max(scaled_opens[j], scaled_closes[j]) and graph_height - i - 1 >= min(scaled_opens[j], scaled_closes[j]):
                        line += color + '█'
                    elif graph_height - i - 1 <= scaled_highs[j] and graph_height - i - 1 >= scaled_lows[j]:
                        line += color + '|'
                    else:
                        line += ' '
                    previous_color = color
                else:
                    line += ' '
            else:
                line += ' '
        line += "\033[1;37;40m" + " " * (border_width - graph_width - 8) + "|"
        print(line)
    print("+" + "-" * border_width + "+\033[0m")

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def main():
    config = load_config()
    symbol = config['symbol']
    mode = config['mode']
    timeframe = config.get('timeframe', '1m')

    prices = []
    while True:
        start_time = time.time()
        config = load_config()
        symbol = config['symbol']
        mode = config['mode']
        timeframe = config.get('timeframe', '1m')
        terminal_size = shutil.get_terminal_size((80, 20))
        limit = max(int(terminal_size.columns * 0.7), 1)
        if mode == 'realtime':
            price = fetch_price(symbol)
            if price is not None:
                prices.append(price)
                if len(prices) > 1000:
                    prices.pop(0)
                draw_realtime_graph(prices[-limit:], symbol)
        elif mode == 'ohlcv':
            ohlcv_data = fetch_ohlcv_data(symbol, timeframe, limit)
            if ohlcv_data is not None:
                current_time = datetime.now()
                next_candle_time = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
                time_remaining = (next_candle_time - current_time).seconds
                draw_candlestick_graph(ohlcv_data, symbol, timeframe)
                print(f"Time remaining: {time_remaining} seconds")
        print("Delay:", round(time.time() - start_time, 2), "seconds")

if __name__ == "__main__":
    print("Starting the program...")
    main()
