from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping():
    """Test that /ping endpoint consistently returns 200 with pong: true"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}

def test_ping_multiple_calls():
    """Test that /ping is stable across multiple calls (no time-based failures)"""
    for _ in range(5):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
