import os, logging, requests, re
from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS
from rag_system import SimpleRAG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize Groq Client
api_key = os.environ.get("GROQ_API_KEY")
if api_key:
    api_key = api_key.strip()
client = Groq(api_key=api_key) if api_key else None

# Initialize RAG
rag_system = SimpleRAG('financial_corpus/sample_docs.txt')

def get_market_data(query):
    # Basic extraction for uppercase stock tickers (e.g. AAPL, TSLA, INFY)
    match = re.search(r'\b[A-Z]{2,5}\b', query)
    if match:
        ticker = match.group(0)
        market_data_url = os.environ.get("MARKET_DATA_URL", "http://market-data-service:5000")
        try:
            res = requests.get(f"{market_data_url}/data/{ticker}", timeout=5)
            if res.status_code == 200:
                data = res.json()
                return f"\n[Live Market Data for {ticker}]: {data}\n"
        except Exception as e:
            logger.error(f"Failed to fetch market data for {ticker}: {e}")
    return ""

@app.route('/generate', methods=['POST'])
def generate():
    # 1. Check if API Key exists
    if not client:
        logger.error("GROQ_API_KEY missing.")
        return jsonify({"advice": "System Error: AI Key missing on server."}), 500

    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_query = data.get('user_query')
        task = data.get('task', 'chat')
        
        # 2. Construct Prompt using Agentic RAG
        # Retrieve context from local documents
        rag_docs = rag_system.retrieve_context(user_query)
        context_str = "\n".join(rag_docs) if rag_docs else "No specific local context available."
        
        # Fetch live market data if applicable
        market_context = get_market_data(user_query)
        
        if task == 'plan':
            system_msg = f"You are a Wealth Manager. Provide a structured investment plan.\n\nContext:\n{context_str}{market_context}"
            model = "llama-3.3-70b-versatile"
        else:
            system_msg = f"You are a Financial Analyst. Be concise and helpful.\n\nContext:\n{context_str}{market_context}"
            model = "llama-3.3-70b-versatile"

        logger.info(f"Generating for query: {user_query}")

        # 3. Call Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_query}
            ],
            model=model,
            temperature=0.2,
            max_tokens=500,
        )
        
        result = chat_completion.choices[0].message.content
        return jsonify({"advice": result})

    except Exception as e:
        logger.error(f"Groq Error: {str(e)}")
        # Return JSON even on error, so Gateway doesn't crash
        return jsonify({"advice": "I am having trouble thinking right now. Please try again."}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)