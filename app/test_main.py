import app.main as main_module
from fastapi.testclient import TestClient


client = TestClient(main_module.app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_stable_health_endpoint():
    responses = [client.get("/ping") for _ in range(3)]
    assert all(response.status_code == 200 for response in responses)
    assert all(response.json() == {"pong": True} for response in responses)


def test_ping_fail_demo_endpoint_exists(monkeypatch):
    monkeypatch.setattr(main_module.time, "time", lambda: 3)
    response = client.get("/ping/fail")
    assert response.status_code == 500


def test_ping_fail_demo_can_be_disabled(monkeypatch):
    monkeypatch.setenv("ENABLE_PING_FAILURE_DEMO", "false")
    monkeypatch.setattr(main_module.time, "time", lambda: 3)
    response = client.get("/ping/fail")
    assert response.status_code == 200
    assert response.json() == {"pong": True, "demo": "failure disabled or not triggered"}
