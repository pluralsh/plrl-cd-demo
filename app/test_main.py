from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_reliably_successful():
    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
