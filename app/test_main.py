from types import SimpleNamespace

from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy_when_the_prior_failure_second_is_forced(monkeypatch):
    monkeypatch.setattr(main, "time", SimpleNamespace(time=lambda: 0), raising=False)

    with TestClient(main.app, raise_server_exceptions=False) as test_client:
        responses = [test_client.get("/ping") for _ in range(3)]

    assert [response.status_code for response in responses] == [200, 200, 200]
    assert [response.json() for response in responses] == [{"pong": True}] * 3
