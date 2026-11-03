from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_always_returns_pong(monkeypatch):
    # Keep the clock at a value that triggered the former modulo-based error.
    import app.main as main

    monkeypatch.setattr(
        main, "time", type("Clock", (), {"time": staticmethod(lambda: 0)})(), raising=False
    )

    for _ in range(10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}
