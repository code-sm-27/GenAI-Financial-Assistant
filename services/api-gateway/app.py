# services/api-gateway/app.py
from flask import Flask, request, jsonify, redirect
import requests
import config

app = Flask(__name__)

# Basic health check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API Gateway is healthy"}), 200

# Route to Market Data Service
@app.route('/api/v1/market_data/<symbol>', methods=['GET'])
def get_market_data(symbol):
    try:
        response = requests.get(f"{config.MARKET_DATA_SERVICE_URL}/data/{symbol}")
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Market Data Service is unavailable"}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error communicating with Market Data Service: {e}"}), 500

# Route to User Management Service
@app.route('/api/v1/user/register', methods=['POST'])
def register_user():
    try:
        response = requests.post(f"{config.USER_MANAGEMENT_SERVICE_URL}/user/register", json=request.json)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "User Management Service is unavailable"}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error communicating with User Management Service: {e}"}), 500

# Route to GenAI Inference Service
@app.route('/api/v1/advice/<symbol>', methods=['POST'])
def get_advice(symbol):
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    try:
        # First, fetch stock data from Market Data Service
        market_data_response = requests.get(f"{config.MARKET_DATA_SERVICE_URL}/data/{symbol}")
        market_data_response.raise_for_status()
        stock_data = market_data_response.json()

        # Then, send to GenAI Inference Service
        genai_response = requests.post(f"{config.GENAI_INFERENCE_SERVICE_URL}/advice", json={
            "symbol": symbol,
            "stock_data": stock_data,
            "user_query": user_query
        })
        genai_response.raise_for_status()
        return jsonify(genai_response.json()), genai_response.status_code
    except requests.exceptions.ConnectionError as e:
        return jsonify({"error": f"Service unavailable: {e}"}), 503
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"Backend service error: {e.response.text}"}), e.response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # Runs on port 5000 by default