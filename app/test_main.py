from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping_returns_200():
    response = client.get("/ping")
    assert response.status_code == 200

def test_ping_returns_correct_payload():
    response = client.get("/ping")
    assert response.json() == {"pong": True}

def test_ping_consistent_across_multiple_requests():
    # Test multiple times to ensure no intermittent failures
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
