from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_stable_by_default(monkeypatch):
    monkeypatch.setattr(main, "ENABLE_PING_FAULT", False)

    for mocked_time in (0, 1, 2, 3, 4, 5):
        monkeypatch.setattr(main.time, "time", lambda: mocked_time)
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
