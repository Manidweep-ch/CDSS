from sqlalchemy.orm import sessionmaker
from app.database.engine import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Dependency function for FastAPI to get database session.
    Ensures proper session cleanup after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
