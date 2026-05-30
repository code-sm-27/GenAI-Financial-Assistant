from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to FinSense API Gateway. See /docs for the API schema."}
