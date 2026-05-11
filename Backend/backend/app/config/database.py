"""Database connection and ORM setup."""

import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import QueuePool

from app.config.settings import settings


logger = logging.getLogger(__name__)


# SQLAlchemy declarative base for all models
Base = declarative_base()


# Database engine configuration
engine = create_engine(
    settings.database.postgres_url,
    poolclass=QueuePool,
    pool_size=settings.database.POSTGRES_POOL_SIZE,
    max_overflow=settings.database.POSTGRES_MAX_OVERFLOW,
    echo=settings.app.DEBUG,
    connect_args={"check_same_thread": False},
)


# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """Dependency function for FastAPI to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for manual session management."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.exception("Database session error: %s", e)
        raise
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables."""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.exception("Failed to initialize database: %s", e)
        raise


def drop_db() -> None:
    """Drop all database tables (use with caution)."""
    try:
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("Database tables dropped successfully")
    except Exception as e:
        logger.exception("Failed to drop database tables: %s", e)
        raise


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Set SQLite pragmas for better performance."""
    # This is a placeholder for SQLite-specific optimizations
    # Not needed for PostgreSQL but kept for compatibility
    pass


@event.listens_for(engine, "pool_connect")
def on_pool_connect(dbapi_conn, connection_record):
    """Handle pool connect events."""
    logger.debug("Database connection established")


@event.listens_for(engine, "pool_checkout")
def on_pool_checkout(dbapi_conn, connection_record, connection_proxy):
    """Handle pool checkout events."""
    logger.debug("Database session checked out from pool")


def close_db() -> None:
    """Close all database connections."""
    try:
        engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.exception("Failed to close database connections: %s", e)
        raise
