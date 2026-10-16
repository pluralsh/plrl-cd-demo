from app import main
from fastapi.testclient import TestClient

client = TestClient(main.app, raise_server_exceptions=False)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy_when_fault_injection_is_not_enabled(monkeypatch):
    monkeypatch.delenv(main.PING_FAULT_INJECTION_ENV, raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_is_enabled_with_true(monkeypatch):
    monkeypatch.setenv(main.PING_FAULT_INJECTION_ENV, " TrUe ")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 500
