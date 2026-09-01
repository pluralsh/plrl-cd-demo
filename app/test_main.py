import pytest
from fastapi.testclient import TestClient

from . import main


client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("timestamp", [6, 7])
@pytest.mark.parametrize("flag_value", [None, "false", "malformed"])
def test_ping_does_not_inject_fault_without_truthy_flag(
    monkeypatch, timestamp, flag_value
):
    if flag_value is None:
        monkeypatch.delenv(main.PING_FAULT_INJECTION_ENABLED, raising=False)
    else:
        monkeypatch.setenv(main.PING_FAULT_INJECTION_ENABLED, flag_value)
    monkeypatch.setattr(main.time, "time", lambda: timestamp)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_injects_fault_on_divisible_timestamp_when_enabled(monkeypatch):
    monkeypatch.setenv(main.PING_FAULT_INJECTION_ENABLED, "true")
    monkeypatch.setattr(main.time, "time", lambda: 6)

    response = client.get("/ping")

    assert response.status_code == 500
    assert response.json() == {"detail": "demo ping fault injection enabled"}


def test_ping_succeeds_on_non_divisible_timestamp_when_enabled(monkeypatch):
    monkeypatch.setenv(main.PING_FAULT_INJECTION_ENABLED, "on")
    monkeypatch.setattr(main.time, "time", lambda: 7)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
