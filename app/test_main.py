from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping():
    """Test that /ping endpoint returns 200 and correct response"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}

def test_ping_reliability():
    """Test that /ping endpoint is reliable across multiple calls"""
    # Test multiple times to ensure no intermittent failures
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
