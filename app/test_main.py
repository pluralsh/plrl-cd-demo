import time

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_at_previously_failing_epoch(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 0)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
