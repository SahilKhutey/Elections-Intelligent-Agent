import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Provides a TestClient instance for API integration tests."""
    return TestClient(app)
