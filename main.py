"""
FastAPI Backend for Legal Perplexity 2.0
=========================================

This FastAPI application provides REST API endpoints for the Legal Perplexity system.
It preserves all existing functionality from the Streamlit version while providing
a modern API interface for the React frontend.

Features:
- Constitution Chat API
- Know Your Rights API
- Case Outcome Prediction API
- Legal Research API
- Maintains existing RAG system, vector database, and parsing logic
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import logging
import sys
from pathlib import Path

# Add constitution_chat to path
sys.path.append(str(Path(__file__).parent))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Legal Perplexity 2.0 API",
    description="FastAPI backend for Legal Perplexity constitutional legal assistant",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add exception handler to prevent server crashes
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception caught: {str(exc)}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://localhost:5175",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:3000"
    ],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check response model
class HealthCheckResponse(BaseModel):
    status: str
    message: str
    version: str

@app.get("/", response_model=HealthCheckResponse)
def root():
    """Root endpoint with API information."""
    return HealthCheckResponse(
        status="healthy",
        message="Legal Perplexity 2.0 API is running",
        version="2.0.0"
    )

@app.get("/health", response_model=HealthCheckResponse)
def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        message="All systems operational",
        version="2.0.0"
    )

# Include routers
try:
    from routers import constitution_chat, rights, cases, research
    # Import the new Know Your Rights router
    from features.know_your_rights.backend import router as know_your_rights_router
    
    app.include_router(constitution_chat.router, prefix="/api/chat", tags=["Constitution Chat"])
    app.include_router(know_your_rights_router.router, prefix="/api/know-your-rights", tags=["Know Your Rights"])
    # Temporarily commenting out other routers to isolate the issue
    # app.include_router(rights.router, prefix="/api/rights", tags=["Know Your Rights"]) 
    # app.include_router(cases.router, prefix="/api/cases", tags=["Case Outcome"])
    # app.include_router(research.router, prefix="/api/research", tags=["Legal Research"])
    
    logger.info("Constitution chat and Know Your Rights routers loaded successfully")
    
except ImportError as e:
    logger.warning(f"Some routers could not be loaded: {e}")
    logger.info("API will run with limited functionality")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )