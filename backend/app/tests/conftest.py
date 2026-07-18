import pytest
from app.config import settings

# Override settings for tests if needed, or define standard fixtures
@pytest.fixture(scope="session")
def test_db_url():
    # For testing, we can use an in-memory SQLite database, or run against Postgres
    # Here, we return the configured database URL
    return settings.DATABASE_URL
