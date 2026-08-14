from fastapi.testclient import TestClient

from . import main
from .main import app

client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_consistently_by_default(monkeypatch):
    monkeypatch.delenv("PING_FAULT_INJECTION", raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    responses = [client.get("/ping") for _ in range(10)]

    assert all(response.status_code == 200 for response in responses)
    assert all(response.json() == {"pong": True} for response in responses)


def test_ping_fault_injection_is_explicit(monkeypatch):
    monkeypatch.setenv("PING_FAULT_INJECTION", "true")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 500
