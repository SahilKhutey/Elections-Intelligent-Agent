import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.cache import memory_cache

@pytest.fixture
def client():
    """
    Standard test client fixture for FastAPI app.
    Function-scoped to ensure a fresh app/state for each test.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def reset_cache():
    """
    Automatically clears the memory cache before every test to ensure isolation.
    """
    memory_cache.clear()
    yield
