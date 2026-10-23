import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_when_fault_injection_is_unset(monkeypatch):
    monkeypatch.delenv("PING_FAULT_INJECTION", raising=False)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


@pytest.mark.parametrize("value", ["True", "TRUE", "1", "false"])
def test_ping_ignores_non_exact_fault_injection_values(monkeypatch, value):
    monkeypatch.setenv("PING_FAULT_INJECTION", value)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_requires_exact_true(monkeypatch):
    monkeypatch.setenv("PING_FAULT_INJECTION", "true")

    response = client.get("/ping")

    assert response.status_code == 500
    assert response.json() == {"detail": "synthetic ping fault injected"}
