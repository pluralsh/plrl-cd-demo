from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)
unsafe_client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_deterministic():
    responses = [client.get("/ping") for _ in range(5)]

    assert all(response.status_code == 200 for response in responses)
    assert all(response.json() == {"pong": True} for response in responses)


def test_demo_failure_can_still_fail(monkeypatch):
    monkeypatch.setattr("app.main.time.time", lambda: 3)

    response = unsafe_client.get("/demo-failure")

    assert response.status_code == 500
