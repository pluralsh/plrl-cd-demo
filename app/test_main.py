from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}

def test_ping_consistency():
    # Verify /ping doesn't intermittently fail
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
