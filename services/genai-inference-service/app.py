import os, logging
from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize Groq Client
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

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
        
        # 2. Construct Prompt
        if task == 'plan':
            system_msg = "You are a Wealth Manager. Provide a structured investment plan."
            model = "llama3-70b-8192"
        else:
            system_msg = "You are a Financial Analyst. Be concise and helpful."
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)