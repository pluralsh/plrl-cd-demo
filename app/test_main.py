from types import SimpleNamespace

from fastapi.testclient import TestClient

from . import main
from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_a_stable_response_on_repeated_requests(monkeypatch):
    # Pin the former fault-injection boundary so this would deterministically
    # return 500 before the handler was fixed.
    monkeypatch.setattr(main, "time", SimpleNamespace(time=lambda: 0), raising=False)

    test_client = TestClient(app, raise_server_exceptions=False)
    responses = [test_client.get("/ping") for _ in range(10)]

    assert [(response.status_code, response.json()) for response in responses] == [
        (200, {"pong": True})
    ] * 10
