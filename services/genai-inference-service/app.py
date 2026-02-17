from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    task = data.get('task', 'chat')
    query = data.get('user_query')
    
    if task == 'plan':
        system_msg = "You are a Wealth Manager. Provide a structured table-based investment plan."
        model = "llama3-70b-8192"
    else:
        system_msg = f"You are a Financial Analyst. Data: {data.get('stock_data')}. Use RAG docs context."
        model = "llama-3.3-70b-versatile"

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": query}
        ],
        model=model,
        temperature=0.2,
    )
    return jsonify({"advice": chat_completion.choices[0].message.content})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)