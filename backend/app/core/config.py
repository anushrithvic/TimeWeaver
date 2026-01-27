"""
Application Configuration Module

This module manages all application settings using Pydantic Settings.
Settings are loaded from environment variables and .env files, with fallback
defaults for development. This provides type-safe configuration management
and automatic validation.

Environment Variables:
    DATABASE_URL: PostgreSQL connection string
    API_V1_PREFIX: API version prefix (default: /api/v1)
    PROJECT_NAME: Application name for API docs
    DEBUG: Enable debug mode and auto-reload
    BACKEND_CORS_ORIGINS: Allowed CORS origins (JSON array)
    SECRET_KEY: JWT secret key (Epic 7 - RBAC)
    ALGORITHM: JWT algorithm (Epic 7 - RBAC)
    ACCESS_TOKEN_EXPIRE_MINUTES: JWT expiration time (Epic 7 - RBAC)

Usage:
    from app.core.config import settings
    database_url = settings.DATABASE_URL
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This class uses Pydantic Settings to automatically load configuration
    from environment variables or .env files. All settings have type hints
    for automatic validation and IDE support.
    
    Attributes:
        DATABASE_URL: PostgreSQL database connection string
        API_V1_PREFIX: URL prefix for API v1 endpoints
        PROJECT_NAME: Application name displayed in API documentation
        DEBUG: Debug mode flag for development
        BACKEND_CORS_ORIGINS: List of allowed CORS origins for frontend access
        SECRET_KEY: Secret key for JWT token signing (Epic 7)
        ALGORITHM: Algorithm for JWT encoding (Epic 7)
        ACCESS_TOKEN_EXPIRE_MINUTES: JWT expiration time in minutes (Epic 7)
    """
    
    # Database Configuration
    # PostgreSQL connection string with format: postgresql://user:password@host:port/database
    DATABASE_URL: str = "postgresql://timeweaver_user:timeweaver_password@localhost:5432/timeweaver_db"
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"  # All API routes will be prefixed with this
    PROJECT_NAME: str = "TimeWeaver API"  # Displayed in Swagger UI
    DEBUG: bool = True  # Enable debug mode for development (auto-reload, verbose errors)
    
    # CORS Configuration
    # List of allowed origins for cross-origin requests (Flutter frontend)
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React development server
        "http://localhost:8080",  # Alternative frontend port
        "http://localhost:5173",  # Vite development server
    ]
    
    # Security Configuration (Epic 7 - RBAC & Authentication)
    # WARNING: Change SECRET_KEY in production to a strong random value!
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"  # JWT signing algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # JWT token lifetime
    
    class Config:
        """Pydantic configuration for settings loading."""
        env_file = ".env"  # Load settings from .env file
        case_sensitive = True  # Environment variable names are case-sensitive


# Global settings instance
# Import this instance throughout the application
settings = Settings()
