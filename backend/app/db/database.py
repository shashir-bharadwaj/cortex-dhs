"""
Central SQLAlchemy database configuration.

This file is the single source of truth for:
- database engine
- SQLAlchemy session
- declarative Base
- FastAPI DB dependency
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings
# -------------------------------------------------------------------
# Database URL
# Update this according to your PostgreSQL credentials
# -------------------------------------------------------------------
DATABASE_URL = settings.DATABASE_URL

# -------------------------------------------------------------------
# SQLAlchemy Engine
# -------------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
    echo=False,  # Set to True if you want SQL query logs
    # Larger pool so high-frequency device ingestion can't starve
    # interactive requests (login, dashboard) of DB connections.
    pool_size=20,
    max_overflow=40,
    pool_timeout=10,
    pool_recycle=1800,
)

# -------------------------------------------------------------------
# Session Factory
# -------------------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# -------------------------------------------------------------------
# Base Class for all SQLAlchemy models
# -------------------------------------------------------------------
Base = declarative_base()


# -------------------------------------------------------------------
# FastAPI Dependency
# -------------------------------------------------------------------
def get_db():
    """
    Provides a database session to FastAPI routes.

    Yields:
        Session: SQLAlchemy DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()