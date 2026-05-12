from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_returns_200():
    """Test that /ping returns 200 OK"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}

def test_ping_no_exceptions():
    """Test that /ping never raises exceptions over multiple calls"""
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
