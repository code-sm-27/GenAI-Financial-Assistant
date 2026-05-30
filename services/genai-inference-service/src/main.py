from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("genai-service")

app = FastAPI(title="FinSense GenAI Inference Service")

@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(content={"status": "ok", "service": "genai-inference-service"})
