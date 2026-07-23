import time

from fastapi.testclient import TestClient

from .main import app



def test_read_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_ping_defaults_healthy(monkeypatch):
    monkeypatch.delenv("CHAOS_PING_FAILURE_RATE", raising=False)
    monkeypatch.setattr(time, "time", lambda: 0)

    client = TestClient(app)
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_chaos_can_be_enabled(monkeypatch):
    monkeypatch.setenv("CHAOS_PING_FAILURE_RATE", "1")
    monkeypatch.setattr(time, "time", lambda: 0)

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/ping")

    assert response.status_code == 500
