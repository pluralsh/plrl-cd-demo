from types import SimpleNamespace

from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_always_returns_pong(monkeypatch):
    # The original implementation raised whenever the wall-clock second was divisible by three.
    # Freeze it at such a second so this test deterministically fails if that behavior returns.
    monkeypatch.setattr(main, "time", SimpleNamespace(time=lambda: 0), raising=False)

    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
