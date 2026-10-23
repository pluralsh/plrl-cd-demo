from fastapi.testclient import TestClient
import pytest

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("fault_value", [None, "false", "TRUE", "1"])
def test_ping_succeeds_without_explicit_fault_injection(monkeypatch, fault_value):
    if fault_value is None:
        monkeypatch.delenv("PING_FAULT_INJECTION", raising=False)
    else:
        monkeypatch.setenv("PING_FAULT_INJECTION", fault_value)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_requires_exact_true(monkeypatch):
    monkeypatch.setenv("PING_FAULT_INJECTION", "true")
    fault_client = TestClient(app, raise_server_exceptions=False)

    response = fault_client.get("/ping")

    assert response.status_code == 500
