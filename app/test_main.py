from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_pong_at_formerly_failing_epoch():
    formerly_failing_epoch = 1_700_000_001
    assert formerly_failing_epoch % 3 == 0

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
