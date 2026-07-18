from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# Base class for SQLAlchemy 2.0 Declarative models
class Base(DeclarativeBase):
    pass

# Build engine connection arguments
connect_args = {}
# SQLite requires check_same_thread=False for FastAPI concurrency, but Postgres does not
if "sqlite" in settings.DATABASE_URL:
    connect_args["check_same_thread"] = False

# Initialize the SQLAlchemy Engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args
)

# SessionLocal factory for generating database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# FastAPI Dependency to get database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
