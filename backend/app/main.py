"""
TimeWeaver Backend - Main Application Entry Point

This module initializes the FastAPI application and configures all middleware,
routers, and core application settings. It serves as the central hub for the
TimeWeaver intelligent academic timetabling system.

Features:
    - FastAPI application initialization
    - CORS middleware configuration for Flutter frontend
    - API v1 router integration
    - Health check endpoints
    - Auto-generated API documentation (Swagger UI, ReDoc)

Usage:
    Run with: uvicorn app.main:app --reload
    Or: python -m app.main
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

# Initialize FastAPI application with metadata
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc"  # ReDoc at /redoc
)

# Configure CORS middleware to allow Flutter frontend access
# This enables cross-origin requests from the specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # Allowed frontend origins
    allow_credentials=True,  # Allow cookies/credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the main API v1 router with all entity endpoints
# All routes will be prefixed with /api/v1
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """
    Root endpoint - Application information
    
    Returns basic information about the API including version and documentation URLs.
    Useful for quick health checks and API discovery.
    
    Returns:
        dict: API metadata including message, version, and docs URL
    """
    return {
        "message": "TimeWeaver API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Simple endpoint to verify the API is running and responding to requests.
    Used by load balancers, monitoring systems, and deployment scripts.
    
    Returns:
        dict: Health status indicator
    """
    return {"status": "healthy"}


# Development server configuration
# Only runs when executing this file directly (not via uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Listen on all network interfaces
        port=8000,  # Default port
        reload=settings.DEBUG  # Auto-reload on code changes in debug mode
    )
