import pytest
from sqlalchemy.orm import Session
from app.config import settings

# Attempting to import from db.py which does not exist yet (TDD RED)
from app.infrastructure.persistence.db import get_db, SessionLocal, engine

def test_engine_is_configured():
    # Engine should be initialized
    assert engine is not None
    # Engine should target correct database URL
    assert engine.url.render_as_string(hide_password=False) == settings.DATABASE_URL

def test_session_local_creation():
    # SessionLocal should create valid database sessions
    session = SessionLocal()
    try:
        assert isinstance(session, Session)
    finally:
        session.close()

def test_get_db_generator():
    # get_db is a dependency that yields a database session
    db_generator = get_db()
    try:
        db = next(db_generator)
        assert isinstance(db, Session)
    finally:
        # Cleanup
        try:
            next(db_generator)
        except StopIteration:
            pass
