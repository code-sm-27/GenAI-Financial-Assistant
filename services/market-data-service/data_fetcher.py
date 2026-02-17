# services/market-data-service/data_fetcher.py
#
# This module is responsible for fetching stock data from external sources.
# For this prototype, it uses yfinance, which provides free access to historical
# market data. In a real-world, high-frequency trading (HFT) standard system,
# this would involve direct, licensed data feeds from exchanges for ultra-low latency.

import yfinance as yf
import datetime
import logging

# Configure logging for the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# A very simple in-memory cache for demonstration purposes.
# In a production system, this would be a distributed, high-performance cache
# like Redis (e.g., Google Cloud Memorystore for Redis).
_market_data_cache = {}

def fetch_stock_data(symbol: str, period: str = "1d", interval: str = "1m") -> dict:
    """
    Fetches historical stock data for the given symbol from yfinance.
    Appends '.NS' for NSE-listed stocks to target the Indian market.
    Includes a simple in-memory cache to reduce redundant API calls during rapid testing.

    Args:
        symbol (str): The stock ticker symbol (e.g., "RELIANCE", "TCS").
        period (str): The period of data to fetch (e.g., "1d", "5d", "1mo").
                      Defaults to "1d" for recent data.
        interval (str): The interval of data points (e.g., "1m", "5m", "1h", "1d").
                        Defaults to "1m" for minute-level data.

    Returns:
        dict: A dictionary containing the latest stock data (close, high, low, volume, timestamp).
              Returns an empty dictionary or raises an error if no data is found.

    Raises:
        ValueError: If no data is found for the specified symbol.
        Exception: For other unexpected errors during data fetching.
    """
    full_symbol = f"{symbol.upper()}.NS" # Ensure symbol is uppercase and target NSE
    
    # Simple cache check: If data for this symbol is in cache and is recent enough (e.g., < 60 seconds)
    if full_symbol in _market_data_cache:
        cached_data = _market_data_cache[full_symbol]
        if (datetime.datetime.now() - cached_data['timestamp']).total_seconds() < 60:
            logging.info(f"Returning cached data for {full_symbol}")
            return cached_data['data']

    logging.info(f"Fetching fresh data for {full_symbol} from yfinance (period={period}, interval={interval})...")
    try:
        ticker = yf.Ticker(full_symbol)
        # Fetch the most recent data for the last 'period' with 'interval'
        hist = ticker.history(period=period, interval=interval)

        if hist.empty:
            logging.warning(f"No data found for {full_symbol} with period={period}, interval={interval}.")
            raise ValueError(f"No data found for {symbol}")

        # Get the latest data point from the historical data
        latest = hist.iloc[-1]

        data = {
            "symbol": symbol,
            "latest_close": float(latest["Close"]),
            "high": float(latest["High"]),
            "low": float(latest["Low"]),
            "open": float(latest["Open"]),
            "volume": int(latest["Volume"]),
            "timestamp": latest.name.isoformat() # Timestamp of the data point
        }
        
        # Update the in-memory cache with the fresh data and current timestamp
        _market_data_cache[full_symbol] = {'data': data, 'timestamp': datetime.datetime.now()}
        return data
    except Exception as e:
        logging.error(f"Error fetching data for {full_symbol}: {e}")
        # Re-raise the exception to be handled by the calling service (app.py)
        raise

# Example usage (for testing data_fetcher directly)
if __name__ == '__main__':
    print("--- Testing data_fetcher.py directly ---")
    try:
        # Test fetching minute-level data for a common stock
        reliance_data = fetch_stock_data("RELIANCE", period="1d", interval="1m")
        print("RELIANCE Data (1m interval):\n", reliance_data)
        
        # Test fetching daily data for another stock
        tcs_data = fetch_stock_data("TCS", period="5d", interval="1d")
        print("\nTCS Data (1d interval):\n", tcs_data)
        
        # Test cache hit (should return cached data if called within 60 seconds)
        reliance_data_cached = fetch_stock_data("RELIANCE", period="1d", interval="1m")
        print("\nRELIANCE Data (cached):\n", reliance_data_cached)

        # Test for a non-existent symbol
        try:
            fetch_stock_data("NONEXISTENTSTOCK")
        except ValueError as ve:
            print(f"\nExpected error for non-existent stock: {ve}")

    except ValueError as ve:
        print(f"\nData error during direct test: {ve}")
    except Exception as e:
        print(f"\nAn unexpected error occurred during direct test: {e}")