"""
Main FastAPI Application Entry Point
Production-level crypto trading system backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from app.config import settings
from app.api import trades
from app.integrations.binance_client import BinanceMarketAggregator

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global state
market_aggregator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context - startup and shutdown"""
    global market_aggregator
    
    # Startup
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Initialize market aggregator
    try:
        market_aggregator = BinanceMarketAggregator()
        logger.info("✅ Binance Market Aggregator initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Binance: {e}")
    
    yield
    
    # Shutdown
    logger.info(f"🛑 Shutting down {settings.APP_NAME}")
    if market_aggregator:
        await market_aggregator.close()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Production-Level Crypto Trading System with AI Intelligence",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check Endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """API root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "version": settings.APP_VERSION
    }


# Include API routes
app.include_router(trades.router, prefix=f"{settings.API_PREFIX}/trades", tags=["Trades"])


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now().isoformat()
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "error": "Internal Server Error",
        "status_code": 500,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
