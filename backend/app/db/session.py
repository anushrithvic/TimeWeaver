"""
Database Session Management Module

This module configures the async SQLAlchemy engine and session management
for the TimeWeaver application. It provides database connectivity using
asyncpg for asynchronous PostgreSQL operations.

Key Components:
    - Async database engine configuration
    - Session factory for creating database sessions
    - FastAPI dependency for session injection
    - SQLAlchemy declarative base for models

Database Driver:
    Uses asyncpg for high-performance async PostgreSQL connections

Usage:
    from app.db.session import get_db, Base
    
    @router.get("/")
    async def endpoint(db: AsyncSession = Depends(get_db)):
        # Use db session here
        pass
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Convert standard PostgreSQL URL to asyncpg URL
# asyncpg is the async PostgreSQL driver we're using
DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async SQLAlchemy engine
# This manages the connection pool and database interactions
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,  # Log all SQL queries in debug mode
    future=True  # Use SQLAlchemy 2.0 style
)

# Create async session factory
# This factory produces database sessions for each request
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,  # Use async session class
    expire_on_commit=False,  # Don't expire objects after commit (useful for returning data)
    autocommit=False,  # Require explicit commits
    autoflush=False,  # Don't auto-flush before queries
)

# SQLAlchemy declarative base class
# All database models inherit from this base
Base = declarative_base()


# FastAPI dependency for database session injection
async def get_db():
    """
    FastAPI dependency that provides a database session for each request.
    
    This function creates a new database session, yields it to the route handler,
    commits the transaction if successful, or rolls back on error. The session
    is always closed after the request completes.
    
    Yields:
        AsyncSession: Database session for the current request
        
    Example:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            # Yield session to the route handler
            yield session
            # Commit transaction if no exceptions occurred
            await session.commit()
        except Exception:
            # Rollback transaction on any error
            await session.rollback()
            raise  # Re-raise exception to FastAPI error handler
        finally:
            # Always close the session
            await session.close()
