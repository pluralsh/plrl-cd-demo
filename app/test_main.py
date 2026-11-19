from types import SimpleNamespace

from fastapi.testclient import TestClient

from . import main
from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_pong_at_previously_failing_epoch_second(monkeypatch):
    monkeypatch.setattr(main, "time", SimpleNamespace(time=lambda: 0), raising=False)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
