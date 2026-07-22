from fastapi.testclient import TestClient

from .main import app

client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_always_returns_pong():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_demo_fail_returns_500_when_time_is_divisible_by_three():
    response = client.get("/demo/fail?now=3")
    assert response.status_code == 500


def test_demo_fail_returns_success_when_time_is_not_divisible_by_three():
    response = client.get("/demo/fail?now=4")
    assert response.status_code == 200
    assert response.json() == {"ok": True, "demo": "healthy"}
