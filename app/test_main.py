from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_200():
    """Test that /ping always returns HTTP 200."""
    # Call multiple times to ensure consistent behavior (no more randomness)
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200


def test_ping_returns_correct_json():
    """Test that /ping returns JSON body with {"pong": true}."""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert data == {"pong": True}


def test_healthz_returns_200():
    """Test that /healthz always returns HTTP 200."""
    response = client.get("/healthz")
    assert response.status_code == 200


def test_healthz_returns_correct_json():
    """Test that /healthz returns JSON body with {"status": "healthy"}."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert data == {"status": "healthy"}
