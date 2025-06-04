# services/genai-inference-service/app.py
from flask import Flask, request, jsonify
from rag_system import SimpleRAG
from llm_client import VertexAILLMClient
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration for Vertex AI (ideally from environment variables in production)
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id-from-env")
VERTEX_AI_ENDPOINT_ID = os.getenv("VERTEX_AI_ENDPOINT_ID", "your-vertex-ai-endpoint-id-from-env")
VERTEX_AI_LOCATION = os.getenv("VERTEX_AI_LOCATION", "us-central1") # Or your region

# Initialize RAG system
CORPUS_PATH = os.path.join(os.path.dirname(__file__), 'financial_corpus', 'sample_docs.txt')
rag_system = SimpleRAG(CORPUS_PATH)

# Initialize LLM client
# if GCP_PROJECT_ID == "your-gcp-project-id-from-env" or VERTEX_AI_ENDPOINT_ID == "your-vertex-ai-endpoint-id-from-env":
#     logging.error("GCP_PROJECT_ID or VERTEX_AI_ENDPOINT_ID not set. LLM client will not be functional.")
#     llm_client = None
# else:
#     llm_client = VertexAILLMClient(GCP_PROJECT_ID, VERTEX_AI_ENDPOINT_ID, VERTEX_AI_LOCATION)
llm_client = None
# Basic health check
@app.route('/health', methods=['GET'])
def health_check():
    status = "GenAI Inference Service is healthy (running in MOCKED LLM mode)"
    return jsonify({"status": status}), 200

@app.route('/advice', methods=['POST'])
def get_investment_advice():
    data = request.get_json()
    symbol = data.get('symbol')
    stock_data = data.get('stock_data')
    user_query = data.get('user_query')

    if not all([symbol, stock_data, user_query]):
        return jsonify({"error": "Missing required parameters: symbol, stock_data, user_query"}), 400

    # if llm_client is None:
    #     return jsonify({"error": "AI service not configured. Please set GCP_PROJECT_ID and VERTEX_AI_ENDPOINT_ID environment variables."}), 500

    try:
            # --- MOCKED LLM LOGIC ---
        # Step 1: Retrieve context from RAG system based on user query
        retrieved_context = rag_system.retrieve_context(user_query)
        context_str = "\n".join(retrieved_context)

        # Step 2: Generate a MOCKED prompt response
        # This is where the magic happens for zero-cost!
        mock_advice = f"Based on your query '{user_query}' and data for {symbol} (Close: {stock_data.get('latest_close')}, Volume: {stock_data.get('volume')}), "

        if "SIP" in user_query.upper() and any("SIP" in c for c in retrieved_context):
            mock_advice += "SIPs are excellent for rupee cost averaging and long-term wealth creation, as detailed in our financial knowledge base."
        elif "SEBI" in user_query.upper() and any("SEBI" in c for c in retrieved_context):
            mock_advice += "SEBI is the primary regulator for the Indian capital market, ensuring investor protection and market development."
        elif stock_data.get('latest_close', 0) > 1000 and stock_data.get('volume', 0) > 5000000:
            mock_advice += f"the stock {symbol} shows strong performance and high liquidity. Consider a 'HOLD' with potential for 'BUY' on dips. (Mocked advice)"
        else:
            mock_advice += "this is a general investment query. Please consult a human financial advisor for personalized advice. (Mocked advice from local system)"

        if context_str:
            mock_advice += f"\n\nContext used from internal knowledge base:\n{context_str}"
        # --- END MOCKED LLM LOGIC ---

        return jsonify({"symbol": symbol, "user_query": user_query, "advice": mock_advice, "context_used": retrieved_context}), 200
    except Exception as e:
        logging.error(f"Error generating advice: {e}")
        return jsonify({"error": f"Failed to generate advice: {e}"}), 500

if __name__ == '__main__':
    # Running on a different port from other services
    app.run(host='0.0.0.0', port=5003)