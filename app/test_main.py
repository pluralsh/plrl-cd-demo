from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)
no_raise_client = TestClient(main.app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_stable(monkeypatch):
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_demo_fail_sometimes_returns_500_when_time_divisible_by_three(monkeypatch):
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = no_raise_client.get("/demo/fail-sometimes")

    assert response.status_code == 500


def test_demo_fail_sometimes_returns_pong_otherwise(monkeypatch):
    monkeypatch.setattr(main.time, "time", lambda: 4)

    response = client.get("/demo/fail-sometimes")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
