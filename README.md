# FinSense - Institutional-Grade Distributed GenAI Financial Intelligence Platform

FinSense is a powerful, distributed financial intelligence platform utilizing agentic RAG and real-time market data. Built with an institutional-grade microservices architecture.

## Architecture

![Architecture Diagram](https://via.placeholder.com/800x400.png?text=FinSense+Architecture)

The system consists of three microservices and a frontend:
1. **Frontend (React 18 + Vite + TS + Tailwind)**: Modern, responsive UI.
2. **API Gateway (FastAPI)**: Central entry point, handles JWT Authentication, rate limiting, and request routing.
3. **GenAI Inference Service (FastAPI)**: Integrates with Groq (Llama-3) for Agentic RAG capabilities.
4. **Market Data Service (FastAPI)**: Handles integration with yFinance/Alpha Vantage, using Redis for rate-limit protection and caching.

**Infrastructure**: PostgreSQL (relational data), Redis (caching).

## Setup Instructions

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend dev, optional if using Docker)
- Python 3.12+

### 1. Environment Variables
Copy the template `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
# Edit .env with your Groq and Alpha Vantage API keys
```

### 2. Run Locally
The easiest way to run the entire stack locally is via Docker Compose:
```bash
docker-compose up --build
```
This spins up:
- PostgreSQL on `5432`
- Redis on `6379`
- API Gateway on `http://localhost:5000`
- Market Data Service on `http://localhost:5001`
- GenAI Service on `http://localhost:5002`
- Frontend on `http://localhost:5173`

### 3. API Documentation
Each FastAPI service provides interactive Swagger UI docs:
- API Gateway: `http://localhost:5000/docs`
- GenAI Service: `http://localhost:5002/docs`
- Market Data Service: `http://localhost:5001/docs`

## Continuous Integration
Pushing to the `main` branch triggers the GitHub Actions CI/CD pipeline, which:
1. Lints code with `flake8`
2. Runs unit tests with `pytest`
3. Builds multi-stage Docker images
4. Deploys to Google Cloud Run (Free Tier)

---
*Built to industry standards: Async IO, Pydantic v2 validation, Structured Logging, Health checks, and JWT rotation.*