import time

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app, raise_server_exceptions=False)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_always_returns_pong(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 0)

    for _ in range(3):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
