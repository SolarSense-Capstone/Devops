from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Solar Viability Health Check API")

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "message": "Solar Viability Assessment API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/healthz")
def healthz():
    """Render's health check endpoint"""
    return {"status": "ok"}

@app.get("/api/v1/status")
def api_status():
    return {
        "api": "Solar Viability Assessment",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "healthz": "/healthz",
            "status": "/api/v1/status"
        }
    }