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


def test_ping_response_body():
    """Test that /ping returns expected JSON body."""
    response = client.get("/ping")
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "pong" in data
    assert data["pong"] is True


def test_ping_is_reliable():
    """Test that /ping consistently returns 200 (no intermittent failures)."""
    # Call multiple times to ensure no random failures
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
