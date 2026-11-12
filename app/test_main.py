import time

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_at_former_failure_timestamp(monkeypatch):
    # The old endpoint raised when the Unix timestamp was divisible by three.
    monkeypatch.setattr(time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
