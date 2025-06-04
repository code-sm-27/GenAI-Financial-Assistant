# services/market-data-service/app.py
#
# This Flask application serves as the Market Data Service.
# It exposes an API endpoint to retrieve stock data, leveraging the
# `data_fetcher` module to interact with yfinance.

from flask import Flask, jsonify
from data_fetcher import fetch_stock_data # Import the data fetching logic
import logging # For logging application events and errors

# Configure logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Flask application
app = Flask(__name__)

# --- Health Check Endpoint ---
@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for the Market Data Service.
    Returns a simple status message to indicate the service is running.
    """
    logging.info("Market Data Service health check requested.")
    return jsonify({"status": "Market Data Service is healthy"}), 200

# --- API Endpoint for Stock Data ---
@app.route('/data/<symbol>', methods=['GET'])
def get_data(symbol):
    """
    API endpoint to retrieve the latest stock data for a given symbol.
    It calls the `fetch_stock_data` function and returns the data as JSON.

    Args:
        symbol (str): The stock ticker symbol provided in the URL path.

    Returns:
        JSON response: Contains the stock data on success (HTTP 200).
        JSON error: Contains an error message on failure (HTTP 404 or 500).
    """
    logging.info(f"Received request for market data for symbol: {symbol}")
    try:
        # In a real system, 'period' and 'interval' might be query parameters
        # or defaults based on the type of data required (e.g., tick, 1min, daily).
        # For this prototype, we fetch 1-minute data for the current day.
        stock_data = fetch_stock_data(symbol.upper(), period="1d", interval="1m")
        logging.info(f"Successfully fetched data for {symbol}.")
        return jsonify(stock_data), 200
    except ValueError as e:
        # Handle cases where no data is found for the symbol
        logging.warning(f"Data not found for {symbol}: {e}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        # Catch any other unexpected errors during data fetching
        logging.error(f"Internal server error while fetching data for {symbol}: {e}")
        return jsonify({"error": "Internal server error while fetching market data"}), 500

# --- Application Entry Point ---
if __name__ == '__main__':
    # When running directly, Flask's development server is used.
    # In a Docker container, this is typically managed by a WSGI server like Gunicorn.
    # Set debug=True for development to enable reloader and debugger.
    # Set debug=False for production.
    # Running on a different port (5001) than the API Gateway (5000).
    app.run(host='00.0.0', port=5001, debug=True)