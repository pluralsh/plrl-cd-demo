from fastapi.testclient import TestClient
import pytest

from . import main

client = TestClient(main.app, raise_server_exceptions=False)


@pytest.fixture(autouse=True)
def reset_ping_fault_injection(monkeypatch):
    monkeypatch.setattr(main, "PING_FAULT_INJECTION_EVERY_N_REQUESTS", 0)
    with main._ping_request_lock:
        main._ping_request_count = 0


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy_by_default():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_is_opt_in(monkeypatch):
    monkeypatch.setattr(main, "PING_FAULT_INJECTION_EVERY_N_REQUESTS", 3)

    assert client.get("/ping").status_code == 200
    assert client.get("/ping").status_code == 200
    assert client.get("/ping").status_code == 500
