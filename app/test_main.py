from types import SimpleNamespace

from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_always_succeeds_when_former_modulo_condition_matches(monkeypatch):
    """Regression: timestamps divisible by three must not make /ping fail."""
    monkeypatch.setattr(main, "time", SimpleNamespace(time=lambda: 3), raising=False)

    responses = [client.get("/ping") for _ in range(3)]

    assert [response.status_code for response in responses] == [200, 200, 200]
    assert [response.json() for response in responses] == [{"pong": True}] * 3
