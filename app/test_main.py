from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_endpoint():
    """Test /ping returns success"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}

def test_ping_reliability():
    """Verify /ping is consistently reliable across multiple calls"""
    for _ in range(100):
        response = client.get("/ping")
        assert response.status_code == 200, "Ping endpoint must be 100% reliable"
        assert response.json() == {"pong": True}
