import pytest
from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_without_fault_injection(monkeypatch):
    monkeypatch.delenv("PING_FAULT_INJECTION", raising=False)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_requires_exact_opt_in(monkeypatch):
    monkeypatch.setattr(main.time, "time", lambda: 0)
    monkeypatch.setenv("PING_FAULT_INJECTION", "TRUE")

    assert client.get("/ping").status_code == 200

    monkeypatch.setenv("PING_FAULT_INJECTION", "true")
    with pytest.raises(Exception, match="unknown internal error"):
        client.get("/ping")
