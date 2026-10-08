from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_pong_when_former_failure_branch_is_selected(monkeypatch):
    class Clock:
        @staticmethod
        def time():
            return 3

    monkeypatch.setattr(main, "time", Clock, raising=False)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
