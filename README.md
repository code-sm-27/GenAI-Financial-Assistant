# FinSense: Distributed GenAI Financial Intelligence Platform

[![Deployment Status](https://img.shields.io/badge/Deployment-Live-success?style=for-the-badge&logo=render)](https://api-gateway.onrender.com)
[![Tech Stack](https://img.shields.io/badge/Stack-Flask%20%7C%20Docker%20%7C%20Llama3-blue?style=for-the-badge)](https://github.com/code-sm-27/GenAI-Financial-Assistant)

**FinSense** is an institutional-grade financial assistant that uses **Agentic RAG (Retrieval-Augmented Generation)** to provide real-time stock analysis and personalized investment strategies. Unlike standard chatbots, FinSense grounds its answers in live market data to prevent hallucinations.

🔗 **Live Demo:** [https://api-gateway.onrender.com](https://api-gateway.onrender.com)

---

## 🚀 Key Features

* **Real-Time Market Data:** Integrates with `yFinance` to fetch live stock prices, PE ratios, and market caps during conversation.
* **Agentic RAG Pipeline:** Dynamically injects financial data into the Llama-3 context window for factual accuracy.
* **Microservices Architecture:** Decoupled services for Gateway, Inference, and Data fetching, communicating via REST APIs.
* **Secure Authentication:** Custom JWT-based stateless authentication with a Google-style login UI.
* **Resilient Deployment:** Hosted on **Render** with PostgreSQL persistence and environment-based configuration.

---

## 🏗️ System Architecture

The system is built as a distributed microservices application:

1.  **API Gateway (Flask):** The entry point. Handles user auth (Register/Login), session management, and routing requests to internal services.
2.  **GenAI Inference Service:** Runs the Llama-3 model via Groq API. It processes the user query and synthesizes the final response.
3.  **Market Data Service:** A specialized worker that fetches real-time financial metrics (Stock Prices, News) when requested by the AI.
4.  **Database (PostgreSQL):** Stores user profiles and interaction history.



---

## 🛠️ Tech Stack

* **Backend:** Python 3.9, Flask
* **AI Model:** Llama-3 (via Groq Cloud API)
* **Database:** PostgreSQL (Render Managed)
* **DevOps:** Docker, Docker Compose, GitOps
* **Frontend:** HTML5, JavaScript (ES6), Tailwind CSS
* **Security:** PyJWT, Werkzeug Security, CORS

---

## ⚙️ Installation & Local Setup

To run this project locally using Docker Compose:

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/code-sm-27/GenAI-Financial-Assistant.git](https://github.com/code-sm-27/GenAI-Financial-Assistant.git)
    cd GenAI-Financial-Assistant
    ```

2.  **Configure Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_actual_api_key_here
    SECRET_KEY=any_random_string_for_security
    DATABASE_URL=postgresql://user:pass@db:5432/finsense_db
    ```

3.  **Run with Docker Compose**
    ```bash
    docker-compose up --build
    ```

4.  **Access the App**
    Open your browser to `http://localhost:5000`

---

## ☁️ Deployment (Render)

This project is deployed using a cloud-native workflow on **Render**:

1.  **Database:** Managed PostgreSQL instance on Render.
2.  **Services:**
    * `api-gateway` (Web Service)
    * `gen-ai-financial-assistant` (Web Service)
    * `market-data-service` (Web Service)
3.  **Configuration:** Environment variables (`GROQ_API_KEY`, `DATABASE_URL`) are injected securely via the Render Dashboard, keeping secrets out of the codebase.

---

## 🔮 Future Improvements

* **Portfolio Tracking:** Allow users to save stocks to a dashboard.
* **Voice Interface:** Integration with Whisper AI for voice-to-text financial queries.
* **Technical Charts:** Rendering candlestick charts directly in the chat interface.

---

**Developed by Shivamani Burgu**
*Connect with me on [LinkedIn](https://www.linkedin.com/in/shivamani27/)*