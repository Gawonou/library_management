from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.core.config import settings

# Create SQLAlchemy engine using the DATABASE_URL from environment
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    # For SQLite, add connect_args={'check_same_thread': False}
    connect_args={'check_same_thread': False} if settings.DATABASE_URL.startswith('sqlite') else {}
)

# SessionLocal is a factory for sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()