from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_reliable_when_former_failure_timestamp_is_used(monkeypatch):
    # Epoch second 3 would have triggered the former modulo-based failure path.
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_demo_error_endpoint_returns_internal_server_error():
    client = TestClient(main.app, raise_server_exceptions=False)

    response = client.get("/test/error")

    assert response.status_code == 500
