import time

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_by_default(monkeypatch):
    monkeypatch.delenv("PING_FAIL_ENABLED", raising=False)
    monkeypatch.setattr(time, "time", lambda: 0)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_failure_injection_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setenv("PING_FAIL_ENABLED", "true")
    monkeypatch.setattr(time, "time", lambda: 0)
    failure_client = TestClient(app, raise_server_exceptions=False)

    response = failure_client.get("/ping")

    assert response.status_code == 500
