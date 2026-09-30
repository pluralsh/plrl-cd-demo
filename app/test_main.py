from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_by_default(monkeypatch):
    monkeypatch.delenv("PING_FAILURE_INJECTION", raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_failure_injection_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setenv("PING_FAILURE_INJECTION", "true")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = TestClient(main.app, raise_server_exceptions=False).get("/ping")

    assert response.status_code == 500
