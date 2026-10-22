from fastapi.testclient import TestClient

from . import main


def test_read_root():
    with TestClient(main.app) as client:
        response = client.get("/")

    assert response.status_code == 200


def test_ping_succeeds_by_default(monkeypatch):
    monkeypatch.delenv("PING_FAULT_INJECTION", raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 0)

    with TestClient(main.app, raise_server_exceptions=False) as client:
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_requires_true(monkeypatch):
    monkeypatch.setenv("PING_FAULT_INJECTION", "true")
    monkeypatch.setattr(main.time, "time", lambda: 0)

    with TestClient(main.app, raise_server_exceptions=False) as client:
        response = client.get("/ping")

    assert response.status_code == 500
