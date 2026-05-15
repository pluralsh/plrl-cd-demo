from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping():
    # Test that /ping returns 200 consistently (no intermittent 500s)
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
