import pytest
from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_pong_without_fault_injection(monkeypatch):
    monkeypatch.delenv("PING_FAULT_INJECTION", raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 0)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setenv("PING_FAULT_INJECTION", "true")
    monkeypatch.setattr(main.time, "time", lambda: 0)

    with pytest.raises(Exception, match="unknown internal error"):
        main.test()
