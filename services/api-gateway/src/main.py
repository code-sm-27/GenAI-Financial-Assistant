from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
import logging
import uuid
import time

# Configure structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("api-gateway")

app = FastAPI(
    title="FinSense API Gateway",
    description="Central gateway for FinSense, handling routing, auth, and rate limiting.",
    version="1.0.0"
)

@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    request.state.correlation_id = correlation_id
    
    start_time = time.time()
    logger.info(f"Incoming request {request.method} {request.url} - Correlation-ID: {correlation_id}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Process-Time"] = str(process_time)
    
    logger.info(f"Completed request {request.method} {request.url} - Status: {response.status_code} - Correlation-ID: {correlation_id} - Time: {process_time:.4f}s")
    return response

@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(content={"status": "ok", "service": "api-gateway"})

@app.get("/", tags=["Root"], response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FinSense | API Gateway</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #f8fafc;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }
            .background-elements {
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                overflow: hidden;
                z-index: 0;
            }
            .glow-circle {
                position: absolute;
                border-radius: 50%;
                filter: blur(80px);
                opacity: 0.4;
            }
            .circle-1 { width: 400px; height: 400px; background: #3b82f6; top: -100px; left: -100px; }
            .circle-2 { width: 500px; height: 500px; background: #8b5cf6; bottom: -200px; right: -100px; }
            
            .container {
                position: relative;
                z-index: 1;
                background: rgba(30, 41, 59, 0.7);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 4rem 3rem;
                max-width: 600px;
                text-align: center;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                transform: translateY(20px);
                animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                opacity: 0;
            }
            @keyframes fadeUp {
                to { opacity: 1; transform: translateY(0); }
            }
            h1 {
                font-size: 3.5rem;
                font-weight: 800;
                margin: 0 0 1rem 0;
                background: linear-gradient(to right, #60a5fa, #c084fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -1px;
            }
            .subtitle {
                font-size: 1.25rem;
                color: #cbd5e1;
                margin-bottom: 2.5rem;
                line-height: 1.6;
            }
            .badge {
                display: inline-block;
                background: rgba(59, 130, 246, 0.2);
                color: #60a5fa;
                padding: 0.5rem 1rem;
                border-radius: 9999px;
                font-size: 0.875rem;
                font-weight: 600;
                margin-bottom: 1.5rem;
                border: 1px solid rgba(59, 130, 246, 0.3);
            }
            .btn {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                background: linear-gradient(to right, #3b82f6, #6366f1);
                color: white;
                padding: 1rem 2rem;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1.1rem;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
                box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.5);
            }
            .btn svg {
                width: 20px;
                height: 20px;
                transition: transform 0.3s ease;
            }
            .btn:hover svg {
                transform: translateX(4px);
            }
            .footer {
                margin-top: 3rem;
                font-size: 0.875rem;
                color: #64748b;
            }
        </style>
    </head>
    <body>
        <div class="background-elements">
            <div class="glow-circle circle-1"></div>
            <div class="glow-circle circle-2"></div>
        </div>
        <div class="container">
            <div class="badge">API Gateway Active</div>
            <h1>FinSense</h1>
            <p class="subtitle">Institutional-Grade Distributed GenAI Financial Intelligence Platform.</p>
            <p style="color: #94a3b8; margin-bottom: 2rem; font-size: 1rem;">
                The interactive frontend is currently in development. Technical reviewers are invited to explore the robust backend architecture via the interactive Swagger documentation.
            </p>
            <a href="/docs" class="btn">
                Explore API Docs
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </a>
            <div class="footer">
                FastAPI • Microservices • GenAI RAG
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
