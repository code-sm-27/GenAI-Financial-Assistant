from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("market-data")

app = FastAPI(title="FinSense Market Data Service")

@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(content={"status": "ok", "service": "market-data-service"})
