import pytest
from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["DB"] == "not configured"


def test_ping_is_safe_by_default_at_divisible_timestamp(monkeypatch):
    monkeypatch.delenv("PING_FAULT_INJECTION", raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_is_safe_by_default_at_non_divisible_timestamp(monkeypatch):
    monkeypatch.delenv("PING_FAULT_INJECTION", raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 4)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_fails_at_divisible_timestamp(monkeypatch):
    monkeypatch.setenv("PING_FAULT_INJECTION", "TrUe")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    with pytest.raises(Exception, match="unknown internal error"):
        main.ping()

    response = client.get("/ping")

    assert response.status_code == 500


def test_ping_fault_injection_allows_non_divisible_timestamp(monkeypatch):
    monkeypatch.setenv("PING_FAULT_INJECTION", "true")
    monkeypatch.setattr(main.time, "time", lambda: 4)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
