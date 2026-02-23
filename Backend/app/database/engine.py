from sqlalchemy import create_engine
import os

# Use PostgreSQL in production, SQLite in development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cdss.db")

# Fix for Render PostgreSQL URL (postgres:// -> postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL settings
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
