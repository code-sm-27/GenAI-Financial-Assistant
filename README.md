# 💰 GenAI Financial Assistant

An intelligent, conversational assistant for smarter investing. Powered by Generative AI and real-time financial data, it helps users analyze portfolios, explore investment opportunities, and get actionable insights—just by asking questions.

---

## ✨ Features

- 🧠 **AI-Powered Q&A** – Ask anything about stocks, crypto, ETFs, or finance in natural language.
- 📊 **Portfolio Analysis** – Visualize and understand your portfolio performance.
- 📉 **Market Insights** – Real-time trends, summaries, and predictions using financial data.
- 🔍 **Natural Language Interface** – Easy-to-use chatbot powered by advanced LLMs.
- 🔐 **Secure & Private** – No sensitive data stored. Local-first options available.

---

## 🛠️ Tech Stack

| Layer    | Technology                   |
|----------|------------------------------|
| Frontend | Next.js (React + TypeScript) |
| Backend  | Flask (Python)               |
| AI Model | OpenAI / Gemma / LLaMA       |
| Database | PostgreSQL / MongoDB (optional) |
| Embeddings | FAISS / Pinecone (optional) |

---

## 🚀 Getting Started

### ✅ Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- OpenAI API Key or Local LLM configured
- Financial API Key (Alpha Vantage, Yahoo Finance, etc.)

---

### 🔙 Backend Setup (Flask)

```bash
# Navigate to backend
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

The Flask API will be running on: `http://127.0.0.1:5000`

---

### 🌐 Frontend Setup (Next.js)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:3000`

Configure your API URL in `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:5000
```

---

## 📦 Project Structure

```
genai-financial-assistant/
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   └── requirements.txt
│
├── frontend/
│   ├── pages/
│   ├── components/
│   └── public/
│
└── README.md
```

---

## 💬 Example Queries

- "Should I invest in Tesla right now?"
- "Summarize the latest news on Bitcoin."
- "How did my portfolio perform this week?"
- "What's the safest investment in 2025?"

---

## 🔮 Roadmap

- [ ] OAuth login & secure portfolio sync
- [ ] Support voice input via Web Speech API
- [ ] Dynamic switch between OpenAI, Gemma, and local LLMs
- [ ] React Native / Flutter mobile app
- [ ] Real-time stock/crypto alerts

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# 1. Fork the repository
# 2. Create a new branch
git checkout -b feat/your-feature-name

# 3. Make changes and commit
git commit -m "Add your feature"

# 4. Push your changes
git push origin feat/your-feature-name

# 5. Open a Pull Request
```

---

## 📄 License

This project is licensed under the MIT License.
