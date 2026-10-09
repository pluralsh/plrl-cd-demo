from types import SimpleNamespace

from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_when_formerly_failing_time_is_forced(monkeypatch):
    monkeypatch.setattr(
        main, "time", SimpleNamespace(time=lambda: 3), raising=False
    )

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
