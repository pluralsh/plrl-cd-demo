from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_returns_200():
    """Test that /ping always returns HTTP 200."""
    response = client.get("/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["pong"] is True
    assert "timestamp" in data

def test_ping_consistency():
    """Test that /ping consistently returns 200 across multiple calls."""
    # Call /ping multiple times to verify it never fails
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
