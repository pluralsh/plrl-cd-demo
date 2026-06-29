from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_success_by_default(monkeypatch):
    monkeypatch.delenv(main.PING_FAULT_INJECTION_ENV, raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_returns_deliberate_500(monkeypatch):
    monkeypatch.setenv(main.PING_FAULT_INJECTION_ENV, "true")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 500
    assert response.json() == {"detail": "Deliberate ping fault injection"}
